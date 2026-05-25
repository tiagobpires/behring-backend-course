# Validação da rota e conexão com banco de dados
from factory import api, db
from sqlalchemy import select
from pydantic import BaseModel
from spectree import Response

# Blueprint e acesso aos dados da requisição
from flask import Blueprint, request

# Função para criar JWT token
from flask_jwt_extended import create_access_token

# Modelo para buscarmos o usuário no banco de dados
from models import User

# Esquema com retorno de um campo "msg"
from utils.response_schema import GenericResponse

auth_controller = Blueprint("auth_controller", __name__, url_prefix="/auth")


# Recebimento de informações de login
class LoginMessage(BaseModel):
    username: str
    password: str


# Retorno do Token de acesso
class LoginResponseMessage(BaseModel):
    access_token: str


@auth_controller.post("/login")
@api.validate(
    json=LoginMessage,
    resp=Response(HTTP_200=LoginResponseMessage, HTTP_401=GenericResponse),
    tags=["auth"],
    security={},
)
def login():
    """
    Login in the system
    """

    data = request.json

    user = db.session.scalars(select(User).filter_by(username=data["username"])).first()

    if user and user.verify_password(data["password"]):
        return {
            "access_token": create_access_token(
                identity=user.username, expires_delta=None
            )
        }

    return {"msg": "Username and password do not match."}, 401
