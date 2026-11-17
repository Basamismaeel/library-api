from repositories import book_repository
from utils import checks
from utils.validation import require_fields


def to_dict(book):
    return {
        "id": book["id"],
        "title": book["title"],
        "author": book["author"],
        "isbn": book["isbn"],
        "available": bool(book["available"]),
    }


def list_books(available_only=False):
    return [to_dict(b) for b in book_repository.find_all(available_only)]


def get_book(book_id):
    return to_dict(checks.ensure_found(book_repository.find_by_id(book_id), "book"))


def create_book(data):
    require_fields(data, "title", "author", message="title and author are required")
    checks.ensure_valid_isbn(data.get("isbn"))
    return to_dict(book_repository.create(data["title"], data["author"], data["isbn"]))


def delete_book(book_id):
    book = checks.ensure_found(book_repository.find_by_id(book_id), "book")
    checks.ensure_book_deletable(book)
    book_repository.delete(book_id)
