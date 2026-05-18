from datetime import datetime

from factory import db
from sqlalchemy import select, or_
from flask import Blueprint, jsonify
from flask.globals import request
from models.user import User

user_controller = Blueprint("user_controller", __name__, url_prefix="/users")


@user_controller.get("/<int:user_id>")
def get_user(user_id: int):

    # Consulta
    user = db.session.get(User, user_id)

    if user is None:
        return {"msg": "User not found."}, 404

    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "birthdate": user.birthdate.isoformat() if user.birthdate else None,
        "created_at": user.created_at.isoformat(),
    }, 200


@user_controller.get("/")
def get_users():
    # Consulta
    users = db.session.scalars(select(User)).all()

    # Retorna uma lista com as informações do usuário
    return [
        {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "birthdate": user.birthdate.isoformat() if user.birthdate else None,
            "created_at": user.created_at.isoformat(),
        }
        for user in users
    ], 200


@user_controller.post("/")
def create_user():
    """
    Create user
    """

    data = request.json

    if db.session.scalars(
        select(User).filter(
            or_(
                User.username == data["username"],
                User.email == data["email"],
            ),
        )
    ).first():
        return {"msg": "User already exists."}, 409

    birthdate = None
    if data.get("birthdate") is not None:
        birthdate = datetime.fromisoformat(data["birthdate"])

    user = User(
        username=data["username"],
        email=data["email"],
        birthdate=birthdate,
    )

    db.session.add(user)
    db.session.commit()

    return {"msg": "User created successfully"}, 201


@user_controller.put("/<int:user_id>")
def update_user(user_id: int):
    # Consulta
    user = db.session.get(User, user_id)

    # Checa se usuário existe
    if user is None:
        return {"msg": f"There is no user with id {user_id}"}, 404

    # Dados recebidos
    data = request.json

    # Altera dados do usuário
    user.username = data["username"]
    user.email = data["email"]
    if "birthdate" in data:
        user.birthdate = datetime.fromisoformat(data["birthdate"])

    # Envia informações para o banco de dados
    db.session.commit()

    # Retorna a mensagem
    return {"msg": "User was updated."}, 200


@user_controller.delete("/<int: user_id>")
def delete_user(user_id: int):

    user = db.session.get(User, user_id)

    if user is None:
        return {"msg": "User does not exist."}, 404

    db.session.delete(user)
    db.session.commit()
