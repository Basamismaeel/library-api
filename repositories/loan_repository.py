from database import get_connection


def find_all():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM loans").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def find_by_id(loan_id):
    conn = get_connection()
    row = conn.execute("SELECT * FROM loans WHERE id = ?", (loan_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def find_by_member(member_id):
    conn = get_connection()
    rows = conn.execute("SELECT * FROM loans WHERE member_id = ?", (member_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def find_open_with_details():
    conn = get_connection()
    rows = conn.execute(
        """
        SELECT loans.id AS loan_id, books.title AS title, members.name AS member,
               loans.due_date AS due_date
        FROM loans
        JOIN books ON books.id = loans.book_id
        JOIN members ON members.id = loans.member_id
        WHERE loans.returned = 0
        """
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def create(book_id, member_id, due_date, checked_out):
    """Insert a loan and mark the book unavailable in one transaction."""
    conn = get_connection()
    cur = conn.execute(
        "INSERT INTO loans (book_id, member_id, due_date, checked_out) VALUES (?, ?, ?, ?)",
        (book_id, member_id, due_date, checked_out),
    )
    conn.execute("UPDATE books SET available = 0 WHERE id = ?", (book_id,))
    conn.commit()
    loan_id = cur.lastrowid
    conn.close()
    return find_by_id(loan_id)


def mark_returned(loan_id, book_id, fine):
    conn = get_connection()
    conn.execute("UPDATE loans SET returned = 1, fine = ? WHERE id = ?", (fine, loan_id))
    conn.execute("UPDATE books SET available = 1 WHERE id = ?", (book_id,))
    conn.commit()
    conn.close()
    return find_by_id(loan_id)


def renew(loan_id, new_due_date):
    conn = get_connection()
    conn.execute(
        "UPDATE loans SET due_date = ?, renewals = renewals + 1 WHERE id = ?",
        (new_due_date, loan_id),
    )
    conn.commit()
    conn.close()
    return find_by_id(loan_id)


def mark_fine_paid(loan_id):
    conn = get_connection()
    conn.execute("UPDATE loans SET fine_paid = 1 WHERE id = ?", (loan_id,))
    conn.commit()
    conn.close()
    return find_by_id(loan_id)
