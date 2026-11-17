from datetime import date, timedelta

from notifications import notifier
from repositories import book_repository, loan_repository, member_repository
from utils import checks
from utils.fines import calculate_fine, days_late, money
from utils.validation import require_fields


def to_dict(loan, with_current_fine=False):
    result = {
        "id": loan["id"],
        "book_id": loan["book_id"],
        "member_id": loan["member_id"],
        "due_date": loan["due_date"],
        "returned": bool(loan["returned"]),
        "fine": money(loan["fine"]),
        "fine_paid": bool(loan["fine_paid"]),
        "renewals": loan["renewals"],
        "checked_out": loan["checked_out"],
    }
    if with_current_fine:
        current = loan["fine"] if loan["returned"] else calculate_fine(loan["due_date"])
        result["current_fine"] = money(current)
    return result


def list_loans(overdue_only=False):
    result = []
    for loan in loan_repository.find_all():
        if overdue_only and (loan["returned"] or days_late(loan["due_date"]) <= 0):
            continue
        result.append(to_dict(loan, with_current_fine=True))
    return result


def get_loan(loan_id):
    loan = checks.ensure_found(loan_repository.find_by_id(loan_id), "loan")
    return to_dict(loan, with_current_fine=True)


def create_loan(data):
    require_fields(data, "book_id", "member_id", message="book_id and member_id are required")
    checks.ensure_valid_due_date(data.get("due_date"))

    book = checks.ensure_found(book_repository.find_by_id(data["book_id"]), "book")
    member = checks.ensure_found(member_repository.find_by_id(data["member_id"]), "member")
    checks.ensure_book_available(book)
    checks.ensure_can_borrow(member, loan_repository.find_by_member(member["id"]))

    today = date.today()
    due_date = data.get("due_date") or (today + timedelta(days=14)).isoformat()
    loan = loan_repository.create(book["id"], member["id"], due_date, today.isoformat())

    notifier.checkout(member["email"], book["title"])
    return to_dict(loan)


def return_loan(loan_id):
    loan = checks.ensure_found(loan_repository.find_by_id(loan_id), "loan")
    checks.ensure_not_returned(loan)

    fine = calculate_fine(loan["due_date"])
    updated = loan_repository.mark_returned(loan_id, loan["book_id"], fine)

    member = member_repository.find_by_id(loan["member_id"])
    book = book_repository.find_by_id(loan["book_id"])
    notifier.returned(member["email"], book["title"], money(fine))
    return to_dict(updated)


def renew_loan(loan_id):
    loan = checks.ensure_found(loan_repository.find_by_id(loan_id), "loan")
    checks.ensure_renewable(loan)

    new_due = (date.fromisoformat(loan["due_date"]) + timedelta(days=14)).isoformat()
    updated = loan_repository.renew(loan_id, new_due)

    member = member_repository.find_by_id(loan["member_id"])
    book = book_repository.find_by_id(loan["book_id"])
    notifier.renewal(member["email"], book["title"])
    return to_dict(updated)


def pay_fine(loan_id):
    loan = checks.ensure_found(loan_repository.find_by_id(loan_id), "loan")
    checks.ensure_payable(loan)

    updated = loan_repository.mark_fine_paid(loan_id)

    member = member_repository.find_by_id(loan["member_id"])
    notifier.fine_paid(member["email"], money(loan["fine"]))
    return to_dict(updated)
