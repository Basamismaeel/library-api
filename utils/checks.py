"""Business-rule checks. Each raises ApiError when the rule is violated."""
from datetime import date

from errors import ApiError
from utils.fines import loan_limit, summarize_loans
from utils.validation import is_valid_date, is_valid_email, is_valid_isbn, is_valid_member_type


def ensure_found(item, name):
    if item is None:
        raise ApiError(name + " not found", 404)
    return item


def ensure_valid_isbn(isbn):
    if not is_valid_isbn(isbn):
        raise ApiError("invalid isbn", 400)


def ensure_valid_email(email):
    if not is_valid_email(email):
        raise ApiError("invalid email", 400)


def ensure_valid_member_type(member_type):
    if not is_valid_member_type(member_type):
        raise ApiError("type must be student or staff", 400)


def ensure_valid_due_date(due_date):
    if due_date and not is_valid_date(due_date):
        raise ApiError("invalid due_date", 400)


def ensure_book_deletable(book):
    if not book["available"]:
        raise ApiError("book is on loan", 409)


def ensure_book_available(book):
    if not book["available"]:
        raise ApiError("book is not available", 409)


def ensure_email_unique(existing):
    if existing is not None:
        raise ApiError("email already registered", 409)


def ensure_can_borrow(member, member_loans):
    open_loans, owed = summarize_loans(member_loans)
    if owed > 0:
        raise ApiError("member has unpaid fines", 409)
    if open_loans >= loan_limit(member["type"]):
        raise ApiError("loan limit reached", 409)


def ensure_not_returned(loan):
    if loan["returned"]:
        raise ApiError("loan already returned", 409)


def ensure_renewable(loan):
    ensure_not_returned(loan)
    if date.fromisoformat(loan["due_date"]) < date.today():
        raise ApiError("overdue loans cannot be renewed", 409)
    if loan["renewals"] >= 1:
        raise ApiError("loan was already renewed", 409)


def ensure_payable(loan):
    if not loan["returned"]:
        raise ApiError("return the book before paying", 409)
    if loan["fine"] <= 0 or loan["fine_paid"]:
        raise ApiError("no fine to pay", 409)
