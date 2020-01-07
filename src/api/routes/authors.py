from flask import Blueprint
from flask import request
from src.api.utils.responses import response_with
import src.api.utils.responses as resp
from src.api.models.authors import Author, AuthorSchema
from src.api.utils.database import db
from flask_jwt_extended import jwt_required  # https://flask-jwt-extended.readthedocs.io/en/stable/api/#flask_jwt_extended.jwt_required

# Configure the Blueprint --> https://exploreflask.com/en/latest/blueprints.html
author_routes = Blueprint("author_routes", __name__)

# =============================== #
# Defining the author API methods
# =============================== #
@author_routes.route("/", methods = ["POST"])
@jwt_required
def create_author():
    try:
        data = request.get_json()
        author_schema = AuthorSchema()
        author = author_schema.load(data)
        result = author_schema.dump(author.create())
        return response_with(resp.SUCCESS_201, value = {"author": result})

    except Exception as err:
        return response_with(resp.INVALID_INPUT_422)


@author_routes.route("/", methods = ["GET"])
@jwt_required
def get_author_list():
    fetched = Author.query.all()
    author_schema = AuthorSchema(many = True, only = ["first_name", "last_name", "id"])
    authors = author_schema.dump(fetched)
    return response_with(resp.SUCCESS_200, value = {"authors": authors})


@author_routes.route("/<int:author_id>", methods = ["GET"])
@jwt_required
def get_author_detail(author_id):
    fetched = Author.query.get_or_404(author_id)
    author_schema = AuthorSchema()
    author = author_schema.dump(fetched)
    return response_with(resp.SUCCESS_200, value={"author": author})


@author_routes.route("/<int:author_id>", methods = ["PUT"])
@jwt_required
def update_author_detail(author_id):
    data = request.get_json()
    author = Author.query.get_or_404(author_id)
    author.first_name = data.get("first_name")
    author.last_name = data.get("last_name")
    db.session.add(author)
    db.session.commit()
    author_schema = AuthorSchema()
    author = author_schema.dump(author)
    return response_with(resp.SUCCESS_200, value={"author": author})


@author_routes.route("/<int:author_id>", methods = ["PATCH"])
@jwt_required
def modify_author_detail(author_id):
    data = request.get_json()
    author = Author.query.get_or_404(author_id)
    if data.get("first_name"):
        author.first_name = data.get("first_name")
    if data.get("last_name"):
        author.last_name = data.get("last_name")
    db.session.add(author)
    db.session.commit()
    author_schema = AuthorSchema()
    author = author_schema.dump(author)
    return response_with(resp.SUCCESS_200, value={"author": author})


@author_routes.route("/<int:author_id>", methods = ["DELETE"])
@jwt_required
def delete_author(author_id):
    author = Author.query.get_or_404(author_id)
    db.session.delete(author)
    db.session.commit()
    return response_with(resp.SUCCESS_204)