import streamlit as st
import pandas as pd
from scheduler import Scheduler
from config import GUARDS_DB
from main import generate_pdf_report # Reusing PDF logic
import os

# Page Config
st.set_page_config(page_title="Security Scheduler Enterprise", layout="wide")

# Title and Header
st.title("🛡️ Security Scheduler Enterprise Edition")
st.markdown("### Automated Workforce Optimization System")

# --- Sidebar Controls ---
st.sidebar.header("Configuration")

# 1. Active Guards Filter
all_guard_names = [g["name"] for g in GUARDS_DB]
selected_guards = st.sidebar.multiselect(
    "Select Active Guards",
    options=all_guard_names,
    default=all_guard_names,
    help="Deselect guards who are unavailable (sick, leave, etc.)"
)

# 2. Overtime Budget (Visual Only)
overtime_budget = st.sidebar.number_input(
    "Weekly Overtime Budget ($)",
    min_value=0,
    value=0,
    step=100,
    help="Target budget for overtime (currently strict 40hr limit enforced)"
)

st.sidebar.markdown("---")
st.sidebar.info("Powered by Google OR-Tools")

# --- Main Area ---

if st.button("🚀 Generate Optimal Schedule", type="primary"):
    with st.spinner("Optimizing schedule with Constraint Programming..."):
        # Initialize Scheduler with selected guards
        scheduler = Scheduler(active_guards_names=selected_guards)
        scheduler.generate_schedule()
        
        # Get Results
        df = scheduler.get_schedule_df()
        summary = scheduler.get_summary()

    # --- Metrics Row ---
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(label="Total Weekly Cost", value=f"${summary['total_cost']:,.2f}")
    
    with col2:
        unfilled_count = len(summary['unfilled_shifts'])
        delta_color = "normal" if unfilled_count == 0 else "inverse"
        st.metric(label="Unfilled Shifts", value=unfilled_count, delta="-0" if unfilled_count == 0 else f"-{unfilled_count}", delta_color=delta_color)
        
    with col3:
        # Efficiency: Avg Hourly Rate
        st.metric(label="Avg Hourly Rate", value=f"${summary['efficiency_avg_rate']:.2f}")

    # --- Status Message ---
    if summary['status'] in ["OPTIMAL", "FEASIBLE"]:
        st.success(f"Optimization Successful! Status: {summary['status']}")
    else:
        st.error(f"Optimization Failed. Status: {summary['status']}")
        if summary['unfilled_shifts']:
            st.warning("Could not fill the following shifts (likely due to missing qualifications or guard shortage):")
            st.write(summary['unfilled_shifts'])

    # --- Schedule Table ---
    if not df.empty:
        st.subheader("Weekly Roster")
        st.dataframe(df, use_container_width=True)
        
        # --- Download Section ---
        # Generate PDF
        pdf_filename = "Weekly_Schedule.pdf"
        generate_pdf_report(df, summary, filename=pdf_filename)
        
        with open(pdf_filename, "rb") as pdf_file:
            pdf_bytes = pdf_file.read()
            
        st.download_button(
            label="📄 Download PDF Report",
            data=pdf_bytes,
            file_name="Weekly_Schedule.pdf",
            mime="application/pdf"
        )
        
    # --- Guard Stats ---
    st.subheader("Guard Utilization")
    stats_df = pd.DataFrame(summary['guard_stats'], columns=["Name", "Hours", "Total Pay"])
    st.bar_chart(stats_df.set_index("Name")["Hours"])
    st.dataframe(stats_df)

else:
    st.info("Click 'Generate Optimal Schedule' to run the optimization engine.")
