from flask import Blueprint
from flask import request
from src.api.utils.responses import response_with
import src.api.utils.responses as resp
from src.api.models.books import Book, BookSchema
from src.api.utils.database import db

# Configure the Blueprint --> https://exploreflask.com/en/latest/blueprints.html
book_routes = Blueprint("book_routes", __name__)

# =============================== #
# Defining the author API methods
# =============================== #
@book_routes.route("/", methods = ["POST"])
def create_book():
    try:
        data = request.get_json()
        schema = BookSchema()
        book = schema.load(data)
        result = schema.dump(book.create())
        return response_with(resp.SUCCESS_201, value = {"book": result})

    except Exception as err:
        print(err)
        return response_with(resp.INVALID_INPUT_422)


@book_routes.route("/", methods = ["GET"])
def get_book_list():
    fetched = Book.query.all()
    schema = BookSchema(many = True, only = ["title", "year", "author_id"])
    books = schema.dump(fetched)
    return response_with(resp.SUCCESS_200, value = {"books": books})


@book_routes.route("/<int:id>", methods = ["GET"])
def get_book_detail(id):
    fetched = Book.query.get_or_404(id)
    schema = BookSchema()
    book = schema.dump(fetched)
    return response_with(resp.SUCCESS_200, value={"book": book})


@book_routes.route("/<int:id>", methods = ["PUT"])
def update_book_detail(id):
    data = request.get_json()
    book = Book.query.get_or_404(id)
    book.author_id = data.get("author_id")
    book.year = data.get("year")
    book.title = data.get("title")
    db.session.add(book)
    db.session.commit()
    schema = BookSchema()
    book = schema.dump(book)
    return response_with(resp.SUCCESS_200, value={"book": book})


@book_routes.route("/<int:id>", methods = ["PATH"])
def modify_book_detail(id):
    data = request.get_json()
    book = Book.query.get_or_404(id)
    if data.get("author_id"):
        book.author_id = data.get("author_id")
    if data.get("year"):
        book.year = data.get("year")
    if data.get("title"):
        book.title = data.get("title")
    db.session.add(book)
    db.session.commit()
    schema = BookSchema()
    book = schema.dump(book)
    return response_with(resp.SUCCESS_200, value={"book": book})


@book_routes.route("/<int:id>", methods = ["DELETE"])
def delete_book(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    return response_with(resp.SUCCESS_204)