from flask import request
from flask_bcrypt import generate_password_hash
import datetime
import json
import jwt

from ..extensions import db
from ..models.User import User, UserSchema
from ..models.UserProfile import UserProfile
from ..config import SECRET_KEY
from ..models.User import User

from ..validators.users import (
    CreateLoginInputSchema,
    CreateSignupInputSchema, 
)
from ..utilities.common import generate_response
from ..utilities.http_code import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

user_schema = UserSchema()


def register_user():
    """
    It creates a new user
    :param request: The request object
    :param input_data: This is the data that is passed to the function
    :return: A response object
    """
    input_data = request.get_json()

    create_validation_schema = CreateSignupInputSchema()
    errors = create_validation_schema.validate(input_data)
    if errors:
        return generate_response(message=errors)
    check_username_exist = User.query.filter_by(
        username=input_data["username"]
    ).first()
    check_email_exist = User.query.filter_by(email=input_data["email"]).first()
    if check_username_exist:
        return generate_response(
            message="Username already exists", status=HTTP_400_BAD_REQUEST
        )
    elif check_email_exist:
        return generate_response(
            message="Email already taken", status=HTTP_400_BAD_REQUEST
        )

    # Create an instance of the User class
    new_user = User(
        username=input_data['username'],
        email=input_data['email'],
        password=input_data['password'],
        is_performer=input_data['is_performer']
    )  

    # new_user_profile = UserProfile(
    #     user_id = new_user.id,
    #     display_name = input_data['username'],
    #     description = "probably a gr8 human"
    # )

    new_user.hash_password()
    db.session.add(new_user)  # Adds new User record to database
    # db.session.add(new_user_profile)
    db.session.commit() 
    del input_data["password"]
    return generate_response(
        data=input_data, message="User Created", status=HTTP_201_CREATED
    )


def login_user():
    """
    It takes in a request and input data, validates the input data, checks if the user exists, checks if
    the password is correct, and returns a response
    :param request: The request object
    :param input_data: The data that is passed to the function
    :return: A dictionary with the keys: data, message, status
    """
    input_data = request.get_json()

    create_validation_schema = CreateLoginInputSchema()
    errors = create_validation_schema.validate(input_data)
    if errors:
        return generate_response(message=errors)

    get_user = User.query.filter_by(username=input_data["username"]).first()
    if get_user is None:
        return generate_response(message="User not found", status=HTTP_400_BAD_REQUEST)
    if get_user.check_password(input_data["password"]):
        token = jwt.encode(
            {
                "id": str(get_user.id),
                "email": get_user.email,
                "username": get_user.username,
                "is_performer": get_user.is_performer,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1),
            },
            SECRET_KEY, algorithm='HS256'
        )
        input_data["token"] = token
        del input_data['password']
        return generate_response(
            data=input_data, message="User login successfully", status=HTTP_201_CREATED
        )
    else:
        return generate_response(
            message="Password is wrong", status=HTTP_400_BAD_REQUEST
        )
