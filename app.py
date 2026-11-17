import os

from flask import Flask

from database import DB_PATH, init_db
from errors import register_error_handlers
from routers import book_router, loan_router, member_router, report_router

app = Flask(__name__)

for router in (book_router, member_router, loan_router, report_router):
    app.register_blueprint(router.bp)
register_error_handlers(app)

if not os.path.exists(DB_PATH):
    init_db()
