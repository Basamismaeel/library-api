from database import get_connection


def find_all():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM members").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def find_by_id(member_id):
    conn = get_connection()
    row = conn.execute("SELECT * FROM members WHERE id = ?", (member_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def find_by_email(email):
    conn = get_connection()
    row = conn.execute("SELECT * FROM members WHERE email = ?", (email,)).fetchone()
    conn.close()
    return dict(row) if row else None


def create(name, email, member_type):
    conn = get_connection()
    cur = conn.execute(
        "INSERT INTO members (name, email, type) VALUES (?, ?, ?)", (name, email, member_type)
    )
    conn.commit()
    member_id = cur.lastrowid
    conn.close()
    return find_by_id(member_id)
