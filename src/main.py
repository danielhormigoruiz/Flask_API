import os
from flask import Flask, jsonify
from src.api.config.config import *
from src.api.utils.database import db
from src.api.utils.responses import response_with
from src.api.models.users import User, UserSchema
import src.api.utils.responses as resp
import logging
from src.api.routes.authors import author_routes
from src.api.routes.books import book_routes
from src.api.routes.users import user_routes
from flask_jwt_extended import JWTManager

# Load the app configuration
if os.environ.get("WORK_ENV") == "PROD":
    app_config = ProductionConfig

elif os.environ.get("WORK_ENV") == "TEST":
    app_config = TestingConfig

else:
    app_config = DevelopmentConfig

# Create the app
app = Flask(__name__)
app.config.from_object(app_config)

# Register the Blueprints
app.register_blueprint(author_routes, url_prefix = "/api/authors")
app.register_blueprint(book_routes, url_prefix = "/api/books")
app.register_blueprint(user_routes, url_prefix = "/api/users")

# Define the global HTTP configs
@app.after_request
def add_header(response):
    return response


@app.errorhandler(400)
def bad_request(e):
    logging.error(e)
    return response_with(resp.BAD_REQUEST_400)


@app.errorhandler(404)
def not_found(e):
    logging.error(e)
    return response_with(resp.SERVER_ERROR_404)


@app.errorhandler(500)
def server_error(e):
    logging.error(e)
    return response_with(resp.SERVER_ERROR_500)


# Initialize the Flask JSON Web Tokens (JWT) manager
app.config['JWT_SECRET_KEY'] = 'HS256'
jwt = JWTManager(app)

# Initialize the db
db.init_app(app)
with app.app_context():
    db.create_all()


# Run the app
if __name__ == "__main__":
    app.run(port = 5000,
            host = "0.0.0.0",
            use_reloader = False)