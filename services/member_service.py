from repositories import loan_repository, member_repository
from utils import checks
from utils.fines import loan_limit, money, summarize_loans
from utils.validation import require_fields


def to_dict(member):
    return {
        "id": member["id"],
        "name": member["name"],
        "email": member["email"],
        "type": member["type"],
    }


def list_members():
    return [to_dict(m) for m in member_repository.find_all()]


def get_member(member_id):
    return to_dict(checks.ensure_found(member_repository.find_by_id(member_id), "member"))


def create_member(data):
    require_fields(data, "name", message="name is required")
    checks.ensure_valid_email(data.get("email"))
    member_type = data.get("type", "student")
    checks.ensure_valid_member_type(member_type)
    checks.ensure_email_unique(member_repository.find_by_email(data["email"]))
    return to_dict(member_repository.create(data["name"], data["email"], member_type))


def get_member_loans(member_id):
    member = checks.ensure_found(member_repository.find_by_id(member_id), "member")
    loans = loan_repository.find_by_member(member_id)
    open_loans, owed = summarize_loans(loans)
    return {
        "loans": [
            {
                "id": loan["id"],
                "book_id": loan["book_id"],
                "due_date": loan["due_date"],
                "returned": bool(loan["returned"]),
                "fine": money(loan["fine"]),
                "fine_paid": bool(loan["fine_paid"]),
            }
            for loan in loans
        ],
        "total_owed": money(owed),
        "loans_remaining": loan_limit(member["type"]) - open_loans,
    }
