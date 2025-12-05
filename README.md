# 🛡️ Security Scheduler Enterprise

**Automated Workforce Optimization System**

Welcome to the **Security Scheduler Enterprise Edition**! This application is designed to demonstrate how "Lean" process optimization and modern Constraint Programming can revolutionize security guard scheduling.

## 🚀 Key Features

*   **Optimal Scheduling**: Uses **Google OR-Tools** to mathematically guarantee the most efficient schedule possible.
*   **Cost Reduction**: Strictly enforces a **40-hour work week** to eliminate overtime costs.
*   **Fairness**: Automatically balances hours among available guards to ensure fair treatment.
*   **Qualification Checks**: Ensures that specialized shifts (e.g., "Night" or "Armed") are only assigned to qualified personnel.
*   **Interactive Dashboard**: A beautiful **Streamlit** interface to manage guards, set budgets, and visualize the roster.
*   **Professional Reporting**: Generates a PDF **Weekly Schedule** ready for print.

## 🛠️ Tech Stack

*   **Python 3.10+**
*   **Streamlit**: For the interactive web dashboard.
*   **Google OR-Tools**: For the constraint programming optimization engine.
*   **Pandas**: For data manipulation.
*   **FPDF**: For PDF report generation.

## 🏁 Getting Started

### 1. Installation

Clone the repository and install the required dependencies:

```bash
git clone https://github.com/ajslaughter/Automated-Scheduler.git
cd Automated-Scheduler
pip install -r requirements.txt
```

### 2. Run the Dashboard

Launch the Enterprise Dashboard with a single command:

```bash
streamlit run app.py
```

This will open the application in your browser (usually at `http://localhost:8501`).

### 3. Generate a Schedule

1.  Use the **Sidebar** to select active guards (simulate sick days by unchecking names).
2.  Click the **"Generate Optimal Schedule"** button.
3.  View the **Metrics** (Cost, Efficiency) and the **Weekly Roster**.
4.  Download the **PDF Report** for your team.

## 📂 Project Structure

*   `app.py`: The main Streamlit application.
*   `scheduler.py`: The logic core containing the OR-Tools optimization model.
*   `config.py`: Configuration settings, simulated database, and shift rules.
*   `main.py`: Legacy CLI entry point (still functional for headless generation).

---

*Built for the Modern Security Manager.*
