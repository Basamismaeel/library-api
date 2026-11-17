from database import get_connection


def find_all(available_only=False):
    conn = get_connection()
    sql = "SELECT * FROM books WHERE available = 1" if available_only else "SELECT * FROM books"
    rows = conn.execute(sql).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def find_by_id(book_id):
    conn = get_connection()
    row = conn.execute("SELECT * FROM books WHERE id = ?", (book_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def create(title, author, isbn):
    conn = get_connection()
    cur = conn.execute(
        "INSERT INTO books (title, author, isbn, available) VALUES (?, ?, ?, 1)",
        (title, author, isbn),
    )
    conn.commit()
    book_id = cur.lastrowid
    conn.close()
    return find_by_id(book_id)


def delete(book_id):
    conn = get_connection()
    conn.execute("DELETE FROM books WHERE id = ?", (book_id,))
    conn.commit()
    conn.close()


def set_available(book_id, available):
    conn = get_connection()
    conn.execute("UPDATE books SET available = ? WHERE id = ?", (1 if available else 0, book_id))
    conn.commit()
    conn.close()


def count():
    conn = get_connection()
    total = conn.execute("SELECT COUNT(*) FROM books").fetchone()[0]
    conn.close()
    return total
