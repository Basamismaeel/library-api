from repositories import book_repository, loan_repository
from utils.fines import calculate_fine, days_late, money, summarize_loans


def overdue_report():
    items = []
    total = 0
    for r in loan_repository.find_open_with_details():
        late = days_late(r["due_date"])
        if late > 0:
            fine = calculate_fine(r["due_date"])
            total += fine
            items.append(
                {
                    "loan_id": r["loan_id"],
                    "title": r["title"],
                    "member": r["member"],
                    "days_late": late,
                    "fine": money(fine),
                }
            )
    return {"items": items, "total_fines": money(total)}


def summary_report():
    loans = loan_repository.find_all()
    on_loan, outstanding = summarize_loans(loans)
    return {
        "total_books": book_repository.count(),
        "on_loan": on_loan,
        "fines_outstanding": money(outstanding),
    }
