import pandas as pd
from fpdf import FPDF
from scheduler import Scheduler
from config import SHIFT_TIMES

def generate_pdf_report(df, summary, filename="Weekly_Schedule.pdf"):
    """
    Generates a professional PDF report using fpdf.
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Weekly Security Guard Schedule", ln=True, align="C")
    
    pdf.set_font("Arial", "", 12)
    pdf.ln(10)
    
    # Summary Section
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Executive Summary", ln=True)
    pdf.set_font("Arial", "", 10)
    pdf.cell(0, 6, f"Total Weekly Cost: ${summary['total_cost']:,.2f}", ln=True)
    pdf.cell(0, 6, f"Total Hours Scheduled: {summary['total_hours']} hrs", ln=True)
    if summary['unfilled_shifts']:
        pdf.set_text_color(255, 0, 0)
        pdf.cell(0, 6, f"WARNING: {len(summary['unfilled_shifts'])} Unfilled Shifts!", ln=True)
        pdf.set_text_color(0, 0, 0)
    else:
        pdf.set_text_color(0, 128, 0)
        pdf.cell(0, 6, "All shifts covered successfully.", ln=True)
        pdf.set_text_color(0, 0, 0)
    
    pdf.ln(10)
    
    # Schedule Table
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Detailed Roster", ln=True)
    
    # Table Header
    pdf.set_font("Arial", "B", 10)
    pdf.set_fill_color(200, 220, 255)
    pdf.cell(30, 10, "Day", 1, 0, "C", 1)
    pdf.cell(30, 10, "Shift", 1, 0, "C", 1)
    pdf.cell(40, 10, "Time", 1, 0, "C", 1)
    pdf.cell(50, 10, "Guard", 1, 0, "C", 1)
    pdf.cell(20, 10, "Hours", 1, 0, "C", 1)
    pdf.cell(20, 10, "Cost", 1, 1, "C", 1)
    
    # Table Rows
    pdf.set_font("Arial", "", 10)
    for index, row in df.iterrows():
        pdf.cell(30, 10, row['Day'], 1)
        pdf.cell(30, 10, row['Shift'], 1)
        pdf.cell(40, 10, SHIFT_TIMES.get(row['Shift'], ""), 1)
        pdf.cell(50, 10, row['Guard'], 1)
        pdf.cell(20, 10, str(row['Hours']), 1, 0, "C")
        pdf.cell(20, 10, f"${row['Cost']:.2f}", 1, 1, "R")
        
    pdf.output(filename)
    print(f"\n[SUCCESS] PDF Report generated: {filename}")

def main():
    print("--- Security Scheduler Automation ---")
    print("Initializing scheduler...")
    
    scheduler = Scheduler()
    scheduler.generate_schedule()
    
    df = scheduler.get_schedule_df()
    summary = scheduler.get_summary()
    
    # Console Report
    print("\n--- Generation Complete ---")
    print(f"Total Cost: ${summary['total_cost']:,.2f}")
    print(f"Total Hours: {summary['total_hours']}")
    
    if summary['unfilled_shifts']:
        print(f"\n[!] WARNING: {len(summary['unfilled_shifts'])} shifts could not be filled!")
        for s in summary['unfilled_shifts']:
            print(f"  - {s}")
    else:
        print("\n[OK] All shifts are fully covered.")
        
    print("\n--- Guard Utilization (Fairness Check) ---")
    for name, hours, pay in summary['guard_stats']:
        print(f"{name:<15}: {hours} hrs | ${pay:,.2f}")

    # Generate PDF
    generate_pdf_report(df, summary)

if __name__ == "__main__":
    main()
