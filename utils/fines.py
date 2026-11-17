"""Fine and loan-limit calculation."""
from datetime import date

FINE_PER_DAY = 0.50
LOAN_LIMITS = {"student": 3, "staff": 5}
DEFAULT_LOAN_LIMIT = 3


def money(x):
    return round(float(x), 2)


def days_late(due_date):
    return (date.today() - date.fromisoformat(due_date)).days


def calculate_fine(due_date):
    """Fine for a loan due on `due_date` if returned today (never negative)."""
    return max(0, days_late(due_date)) * FINE_PER_DAY


def loan_limit(member_type):
    return LOAN_LIMITS.get(member_type, DEFAULT_LOAN_LIMIT)


def summarize_loans(loans):
    """Return (open_loans, total_owed) for a list of loan dicts."""
    owed = 0
    open_loans = 0
    for loan in loans:
        if not loan["returned"]:
            open_loans += 1
            owed += calculate_fine(loan["due_date"])
        elif not loan["fine_paid"]:
            owed += loan["fine"]
    return open_loans, owed
