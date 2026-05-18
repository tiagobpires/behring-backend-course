from datetime import datetime

from factory import db
from main import app
from models import User

from sqlalchemy import select

with app.app_context():

    user = db.session.get(User, 2)

    db.session.delete(user)

    db.session.commit()
