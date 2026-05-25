from datetime import datetime

from factory import db, api
from sqlalchemy import select, or_
from flask import Blueprint, jsonify
from flask.globals import request
from models.user import User, UserCreate, UserResponse, UserResponseList, UserUpdate
from utils.response_schema import GenericResponse
from spectree import Response
from flask_jwt_extended import jwt_required, current_user

user_controller = Blueprint("user_controller", __name__, url_prefix="/users")


@user_controller.get("/<int:user_id>")
@api.validate(
    resp=Response(HTTP_200=UserResponse, HTTP_404=GenericResponse), tags=["users"]
)
@jwt_required()
def get_user(user_id: int):
    """
    Get user by id
    """

    # Consulta
    user = db.session.get(User, user_id)

    if user is None:
        return {"msg": "User not found."}, 404

    response = UserResponse.model_validate(user).to_response_dict()

    return response, 200


@user_controller.get("/")
@api.validate(resp=Response(HTTP_200=UserResponseList), tags=["users"])
@jwt_required()
def get_users():
    """
    Get users
    """
    # Consulta
    users = db.session.scalars(select(User)).all()

    response = UserResponseList(
        users=[UserResponse.model_validate(user) for user in users]
    ).to_response_dict()

    # Retorna uma lista com as informações do usuário
    return response, 200


@user_controller.post("/")
@api.validate(
    json=UserCreate,
    resp=Response(HTTP_201=GenericResponse, HTTP_409=GenericResponse),
    tags=["users"],
    security={},
)
def create_user():
    """
    Create user
    """

    data = request.json

    print(data["username"], data["email"])

    if db.session.scalars(
        select(User).filter(
            or_(User.username == data["username"], User.email == data["email"])
        )
    ).first():
        return {"msg": "User already exists."}, 409

    birthdate = None
    if data.get("birthdate") is not None:
        birthdate = datetime.fromisoformat(data["birthdate"])

    user = User(
        username=data["username"],
        email=data["email"],
        password=data["password"],
        birthdate=birthdate,
    )

    db.session.add(user)
    db.session.commit()

    return {"msg": "User created successfully"}, 201


@user_controller.put("")
@api.validate(
    json=UserUpdate,
    resp=Response(HTTP_200=GenericResponse),
    tags=["users"],
)
@jwt_required()
def update_user():
    """
    Update user

    - Example
    """

    # Dados recebidos
    data = request.json

    # Altera dados do usuário
    current_user.username = data["username"]
    current_user.email = data["email"]
    if "birthdate" in data:
        current_user.birthdate = datetime.fromisoformat(data["birthdate"])

    # Envia informações para o banco de dados
    db.session.commit()

    # Retorna a mensagem
    return {"msg": "User was updated."}, 200


@user_controller.delete("")
@api.validate(resp=Response(HTTP_200=GenericResponse), tags=["users"])
@jwt_required()
def delete_user():
    """
    Delete user
    """

    db.session.delete(current_user)
    db.session.commit()

    return {"msg": "User deleted."}, 200
