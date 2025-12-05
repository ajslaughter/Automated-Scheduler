import pandas as pd
from config import GUARDS_DB, SHIFTS, DAYS, MAX_HOURS_PER_WEEK, SHIFT_DURATION_HOURS

class Guard:
    """
    Represents a security guard.
    Tracks assigned hours and total cost.
    """
    def __init__(self, name, rate):
        self.name = name
        self.rate = rate
        self.hours_assigned = 0
        self.total_pay = 0.0
        self.schedule = {} # Key: Day, Value: Shift

    def can_work(self, hours):
        """Checks if assigning these hours would exceed the weekly limit."""
        # Cost-saving logic: Strictly enforce the 40-hour cap to prevent overtime pay.
        return (self.hours_assigned + hours) <= MAX_HOURS_PER_WEEK

    def assign_shift(self, day, shift, hours):
        """Assigns a shift to the guard and updates their stats."""
        self.hours_assigned += hours
        self.total_pay += hours * self.rate
        self.schedule[day] = shift

    def __repr__(self):
        return f"{self.name} (${self.rate}/hr) - {self.hours_assigned} hrs"


class Scheduler:
    """
    Engine for generating the weekly schedule.
    """
    def __init__(self):
        self.guards = [Guard(g["name"], g["rate"]) for g in GUARDS_DB]
        self.schedule_data = [] # List of dictionaries for DataFrame
        self.unfilled_shifts = []

    def generate_schedule(self):
        """
        Generates the schedule by iterating through every required shift
        and assigning the best available guard.
        """
        for day in DAYS:
            for shift_name in SHIFTS:
                assigned_guard = self._find_best_guard(day, shift_name)
                
                if assigned_guard:
                    assigned_guard.assign_shift(day, shift_name, SHIFT_DURATION_HOURS)
                    self.schedule_data.append({
                        "Day": day,
                        "Shift": shift_name,
                        "Guard": assigned_guard.name,
                        "Hours": SHIFT_DURATION_HOURS,
                        "Cost": SHIFT_DURATION_HOURS * assigned_guard.rate
                    })
                else:
                    self.unfilled_shifts.append(f"{day} - {shift_name}")
                    self.schedule_data.append({
                        "Day": day,
                        "Shift": shift_name,
                        "Guard": "UNFILLED",
                        "Hours": 0,
                        "Cost": 0
                    })

    def _find_best_guard(self, day, shift):
        """
        Finds the most suitable guard for a specific shift.
        Logic:
        1. Filter guards who haven't maxed out hours (Hard Constraint).
        2. Filter guards who aren't already working this day (Simple rule: 1 shift/day for simplicity, though not strictly required by prompt, it's good practice).
        3. Sort by current hours assigned (ascending) to ensure FAIRNESS.
        """
        available_guards = []
        for guard in self.guards:
            # Check hard constraint: Overtime
            if not guard.can_work(SHIFT_DURATION_HOURS):
                continue
            
            # Check if already working this day (prevent double booking)
            if day in guard.schedule:
                continue

            available_guards.append(guard)

        # Fairness Logic: Sort by least hours assigned first.
        # This ensures we distribute hours evenly as we go.
        available_guards.sort(key=lambda x: x.hours_assigned)

        if available_guards:
            return available_guards[0]
        return None

    def get_schedule_df(self):
        """Returns the schedule as a pandas DataFrame."""
        return pd.DataFrame(self.schedule_data)

    def get_summary(self):
        """Returns a summary dictionary."""
        total_cost = sum(g.total_pay for g in self.guards)
        total_hours = sum(g.hours_assigned for g in self.guards)
        
        return {
            "total_cost": total_cost,
            "total_hours": total_hours,
            "unfilled_shifts": self.unfilled_shifts,
            "guard_stats": [(g.name, g.hours_assigned, g.total_pay) for g in self.guards]
        }
