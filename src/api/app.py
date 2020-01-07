from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields

# Configure the app
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:d.54149899X@localhost:3306/landing"

# Configure the database object
db = SQLAlchemy(app)

# ====================================================================== #
#                       Define the class Author
#
# This class is used to define the Author model
# ====================================================================== #


class Author(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    specialization = db.Column(db.String(50))

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, name, specialization):
        self.name = name
        self.specialization = specialization

    def __repr__(self):
        return "Product {}".format(self.id)

# ====================================================================== #
#                       Define the class AuthorSchema
#
# This class is used to print out the results
# ====================================================================== #


class AuthorSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Author
        sqla_session = db.session

    id = fields.Number(dump_only=True)
    name = fields.String(required=True)
    specialization = fields.String(required=True)

# ====================================================================== #
#                       Define the endpoints
# ====================================================================== #
@app.route("/authors", methods = ["GET"])
def index():
    get_authors = Author.query.all()
    author_schema = AuthorSchema(many = True)
    authors = author_schema.dump(get_authors)
    return make_response(jsonify({"authors": authors}))


@app.route("/authors", methods = ["POST"])
def create_author():
    data = request.get_json()
    author_schema = AuthorSchema()
    author = author_schema.load(data)
    result = author_schema.dump(author.create())
    return make_response(jsonify({"author": result}), 201)


@app.route("/authors/<id>", methods = ["GET"])
def get_author_by_id(id):
    get_author = Author.query.get(id)
    author_schema = AuthorSchema(many = False)
    author = author_schema.dump(get_author)
    return make_response(jsonify({"author": author}))


@app.route("/authors/<id>", methods = ["PUT"])
def update_author_by_id(id):
    get_author = Author.query.get(id)
    data = request.get_json()
    if data.get("specialization"):
        get_author.specialization = data.get("specialization")
    if data.get("name"):
        get_author.name = data.get("name")
    db.session.add(get_author)
    db.session.commit()
    author_schema = AuthorSchema(only = ["id", "name", "specialization"])
    result = author_schema.dump(get_author)
    return make_response(jsonify({"author": result}), 201)


@app.route("/authors/<id>", methods = ["DELETE"])
def delete_author_by_id(id):
    get_author = Author.query.get(id)
    db.session.delete(get_author)
    db.session.commit()
    return make_response("", 204)


if __name__ == '__main__':
    # Create the table in the database
    db.create_all()

    # Run the app
    app.run()
