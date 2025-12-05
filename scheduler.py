import pandas as pd
from ortools.sat.python import cp_model
from config import GUARDS_DB, SHIFTS, DAYS, MAX_HOURS_PER_WEEK, SHIFT_DURATION_HOURS, get_shift_requirements

class Guard:
    """
    Represents a security guard.
    Tracks assigned hours and total cost.
    """
    def __init__(self, name, rate, qualifications):
        self.name = name
        self.rate = rate
        self.qualifications = set(qualifications)
        self.hours_assigned = 0
        self.total_pay = 0.0

    def has_qualification(self, required_qual):
        """Checks if the guard has a specific qualification."""
        return required_qual in self.qualifications

    def __repr__(self):
        return f"{self.name} (${self.rate}/hr)"


class Scheduler:
    """
    Engine for generating the weekly schedule using Google OR-Tools.
    This guarantees an OPTIMAL schedule based on constraints.
    """
    def __init__(self, active_guards_names=None):
        # Filter active guards if provided, else use all
        if active_guards_names:
            self.guards = [Guard(g["name"], g["rate"], g["qualifications"]) 
                           for g in GUARDS_DB if g["name"] in active_guards_names]
        else:
            self.guards = [Guard(g["name"], g["rate"], g["qualifications"]) for g in GUARDS_DB]
            
        self.schedule_data = [] # List of dictionaries for DataFrame
        self.unfilled_shifts = []
        self.status = "UNKNOWN"

    def generate_schedule(self):
        """
        Generates the schedule using Constraint Programming (CP-SAT).
        """
        model = cp_model.CpModel()

        # --- Variables ---
        # x[d, s, g] is a boolean variable: 1 if guard g works on day d, shift s; 0 otherwise.
        shifts = {}
        for d, day in enumerate(DAYS):
            for s, shift in enumerate(SHIFTS):
                for g, guard in enumerate(self.guards):
                    shifts[(d, s, g)] = model.NewBoolVar(f'shift_d{d}_s{s}_g{g}')

        # --- Constraints ---

        # 1. Coverage Constraint: Each shift must be assigned to EXACTLY ONE guard.
        # Note: If we have insufficient guards, this model will be INFEASIBLE.
        # To handle this gracefully, we could use soft constraints, but for this "Hard" requirement
        # we will enforce it and report status.
        for d, day in enumerate(DAYS):
            for s, shift in enumerate(SHIFTS):
                model.Add(sum(shifts[(d, s, g)] for g in range(len(self.guards))) == 1)

        # 2. Qualification Constraint: Guard must have required skills for the shift.
        for d, day in enumerate(DAYS):
            for s, shift in enumerate(SHIFTS):
                required_quals = get_shift_requirements(day, shift)
                for g, guard in enumerate(self.guards):
                    for req in required_quals:
                        if not guard.has_qualification(req):
                            # If guard lacks skill, force their variable to 0 for this shift
                            model.Add(shifts[(d, s, g)] == 0)

        # 3. Max Hours Constraint: No guard works > 40 hours.
        # Total shifts per guard * 8 hours <= 40
        # Which simplifies to: Total shifts per guard <= 5
        max_shifts_per_guard = MAX_HOURS_PER_WEEK // SHIFT_DURATION_HOURS
        for g in range(len(self.guards)):
            model.Add(sum(shifts[(d, s, g)] for d in range(len(DAYS)) for s in range(len(SHIFTS))) <= max_shifts_per_guard)

        # --- Objective ---
        # Minimize Total Cost
        # Cost = Sum(Guard Rate * 8 hours * IsAssigned)
        total_cost = sum(
            shifts[(d, s, g)] * int(self.guards[g].rate * SHIFT_DURATION_HOURS)
            for d in range(len(DAYS))
            for s in range(len(SHIFTS))
            for g in range(len(self.guards))
        )
        model.Minimize(total_cost)

        # --- Solve ---
        solver = cp_model.CpSolver()
        status = solver.Solve(model)
        self.status = solver.StatusName(status)

        if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            self._extract_solution(solver, shifts)
        else:
            self.unfilled_shifts.append("Optimization Failed: Constraints could not be met (likely insufficient qualified guards).")

    def _extract_solution(self, solver, shifts):
        """Extracts the schedule from the solver's solution."""
        for d, day in enumerate(DAYS):
            for s, shift in enumerate(SHIFTS):
                is_filled = False
                for g, guard in enumerate(self.guards):
                    if solver.Value(shifts[(d, s, g)]) == 1:
                        guard.hours_assigned += SHIFT_DURATION_HOURS
                        guard.total_pay += SHIFT_DURATION_HOURS * guard.rate
                        
                        self.schedule_data.append({
                            "Day": day,
                            "Shift": shift,
                            "Guard": guard.name,
                            "Qualifications": ", ".join(guard.qualifications),
                            "Hours": SHIFT_DURATION_HOURS,
                            "Cost": SHIFT_DURATION_HOURS * guard.rate
                        })
                        is_filled = True
                        break
                if not is_filled:
                     # This shouldn't happen if status is OPTIMAL/FEASIBLE and coverage constraint is on
                     self.unfilled_shifts.append(f"{day} - {shift}")

    def get_schedule_df(self):
        """Returns the schedule as a pandas DataFrame."""
        return pd.DataFrame(self.schedule_data)

    def get_summary(self):
        """Returns a summary dictionary."""
        total_cost = sum(g.total_pay for g in self.guards)
        total_hours = sum(g.hours_assigned for g in self.guards)
        
        # Calculate Efficiency Score (Simple metric: Cost / Hours)
        # Lower is better, but for "Score" maybe we want 100 - (something).
        # Let's just return the raw Avg Hourly Rate as efficiency metric for now.
        avg_rate = total_cost / total_hours if total_hours > 0 else 0
        
        return {
            "total_cost": total_cost,
            "total_hours": total_hours,
            "unfilled_shifts": self.unfilled_shifts,
            "efficiency_avg_rate": avg_rate,
            "status": self.status,
            "guard_stats": [(g.name, g.hours_assigned, g.total_pay) for g in self.guards]
        }
