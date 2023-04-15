from db import db


class ChatGptRequestModel(db.Model):
    __tablename__ = "requests"

    id = db.Column(db.Integer, primary_key=True)
    request = db.Column(db.String(50000), unique=True, nullable=False)