from db import db


class ChatGptAnswerModel(db.Model):
    __tablename__ = "answers"

    id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.String(50000), unique=True, nullable=False)