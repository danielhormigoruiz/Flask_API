from flask import Blueprint
from flask import request
from src.api.utils.responses import response_with
import src.api.utils.responses as resp
from src.api.models.users import User, UserSchema
from src.api.utils.database import db
from flask_jwt_extended import create_access_token

# Configure the Blueprint --> https://exploreflask.com/en/latest/blueprints.html
user_routes = Blueprint("user_routes", __name__)

# =============================== #
# Defining the author API methods
# =============================== #
@user_routes.route("/", methods = ["POST"])
def create_user():
    try:
        data = request.get_json()
        data['password'] = User.generate_hash(data.get("password"))
        user_schema = UserSchema()
        user = user_schema.load(data)
        user = user_schema.dump(user.create())
        return response_with(resp.SUCCESS_201)

    except Exception as err:
        print(err)
        return response_with(resp.INVALID_INPUT_422)


@user_routes.route("/login", methods = ["POST"])
def authenticate_user():
    try:
        data = request.get_json()
        user = User.find_by_username(data.get("username"))
        if not user:
            return response_with(resp.SERVER_ERROR_404)
        if User.verify_hash(data.get("password"), user.password):
            access_token = create_access_token(identity = data.get("username"))
            return response_with(resp.SUCCESS_201, value = {"message": "Logged in as {}".format(user.username),
                                                            "access_token": access_token})
        else:
            return response_with(resp.UNAUTHORIZED_403)

    except Exception as err:
        print(err)
        return response_with(resp.INVALID_INPUT_422)