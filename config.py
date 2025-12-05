"""
Configuration file for the Security Scheduler application.
Simulates a database of guards and shift requirements.
"""

# Constraints
MAX_HOURS_PER_WEEK = 40
SHIFT_DURATION_HOURS = 8

# Simulated Database of Guards
# Each guard has a name, hourly rate ($), and a list of qualifications.
GUARDS_DB = [
    {"name": "John Smith", "rate": 20.0, "qualifications": ["Level 1", "Armed"]},
    {"name": "Jane Doe", "rate": 22.0, "qualifications": ["Level 1", "Medical"]},
    {"name": "Bob Johnson", "rate": 18.5, "qualifications": ["Level 1"]},
    {"name": "Alice Williams", "rate": 21.0, "qualifications": ["Level 1", "Armed", "Medical"]},
    {"name": "Charlie Brown", "rate": 19.0, "qualifications": ["Level 1"]},
    {"name": "David Miller", "rate": 20.5, "qualifications": ["Level 1", "Armed"]},
    {"name": "Eva Davis", "rate": 23.0, "qualifications": ["Level 1", "Supervisor"]},
    {"name": "Frank Wilson", "rate": 19.5, "qualifications": ["Level 1"]},
    {"name": "Grace Moore", "rate": 21.5, "qualifications": ["Level 1", "Medical"]},
    {"name": "Henry Taylor", "rate": 18.0, "qualifications": ["Level 1"]},
]

# Shift Definitions
# We need 24/7 coverage: Morning, Swing, Night
# Some shifts now require specific qualifications.
SHIFTS = ["Morning", "Swing", "Night"]
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

# Detailed Shift Requirements (Simulated)
# For simplicity, let's say Night shifts require 'Armed' and Morning shifts require 'Medical' on weekends.
# This function helps us determine requirements dynamically.
def get_shift_requirements(day, shift):
    reqs = ["Level 1"] # Base requirement
    if shift == "Night":
        reqs.append("Armed")
    if day in ["Saturday", "Sunday"] and shift == "Morning":
        reqs.append("Medical")
    return reqs

# Shift times for display purposes
SHIFT_TIMES = {
    "Morning": "08:00 - 16:00",
    "Swing": "16:00 - 00:00",
    "Night": "00:00 - 08:00"
}
