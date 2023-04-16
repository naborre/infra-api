from db import db


class ChatGptResponseModel(db.Model):
    __tablename__ = "responses"

    id = db.Column(db.Integer, primary_key=True)
    response = db.Column(db.String(50000), unique=True, nullable=False)
    
    request_id = db.Column(
        db.Integer, db.ForeignKey("requests.id"), unique=False, nullable=False
    )
    request = db.relationship("ChatGptRequestModel", back_populates="responses")