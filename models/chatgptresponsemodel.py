from db import db


class ChatGptResponseModel(db.Model):
    __tablename__ = "responses"

    id = db.Column(db.Integer, primary_key=True)
    response = db.Column(db.String(50000), unique=True, nullable=False)
    
    answer_id = db.Column(
        db.Integer, db.ForeignKey("answers.id"), unique=False, nullable=False
    )
    answer = db.relationship("ChatGptAnswerModel", back_populates="responses")