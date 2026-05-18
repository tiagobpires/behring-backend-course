from pydantic import BaseModel


class GenericResponse(BaseModel):
    msg: str
