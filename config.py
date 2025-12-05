"""
Configuration file for the Security Scheduler application.
Simulates a database of guards and shift requirements.
"""

# Constraints
MAX_HOURS_PER_WEEK = 40
SHIFT_DURATION_HOURS = 8

# Simulated Database of Guards
# Each guard has a name and an hourly rate ($)
GUARDS_DB = [
    {"name": "John Smith", "rate": 20.0},
    {"name": "Jane Doe", "rate": 22.0},
    {"name": "Bob Johnson", "rate": 18.5},
    {"name": "Alice Williams", "rate": 21.0},
    {"name": "Charlie Brown", "rate": 19.0},
    {"name": "David Miller", "rate": 20.5},
    {"name": "Eva Davis", "rate": 23.0},
    {"name": "Frank Wilson", "rate": 19.5},
    {"name": "Grace Moore", "rate": 21.5},
    {"name": "Henry Taylor", "rate": 18.0},
]

# Shift Definitions
# We need 24/7 coverage: Morning, Swing, Night
SHIFTS = ["Morning", "Swing", "Night"]
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

# Shift times for display purposes
SHIFT_TIMES = {
    "Morning": "08:00 - 16:00",
    "Swing": "16:00 - 00:00",
    "Night": "00:00 - 08:00"
}
