from db import db


class ChatGptResponseModel(db.Model):
    __tablename__ = "responses"

    id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.String(50000), unique=True, nullable=False)
    response = db.Column(db.String(50000), unique=True, nullable=False)