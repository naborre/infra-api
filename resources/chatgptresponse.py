from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import ChatGptResponseModel
from schemas import ChatGptResponseSchema, ChatGptResponseUpdateSchema

blp = Blueprint("ChatGptResponses", "chatgptresponses", description="Responses of chatGPT")


@blp.route("/chatgptresponses/<int:response_id>")
class ChatGptResponse(MethodView):
    @blp.response(200, ChatGptResponseModel)
    def get(self, response_id):
        response = ChatGptResponseSchema.query.get_or_404(response_id)
        return response

    def delete(self, response_id):
        response = ChatGptResponseModel.query.get_or_404(response_id)
        db.session.delete(response)
        db.session.commit()
        return {"message": "Response deleted."}

    @blp.arguments(ChatGptResponseUpdateSchema)
    @blp.response(200, ChatGptResponseSchema)
    def put(self, response_data, response_id):
        response = ChatGptResponseModel.query.get(response_id)

        if response:
            response.response = response_data["response"]
        else:
            response = ChatGptResponseModel(id=response_id, **response_data)

        db.session.add(response)
        db.session.commit()

        return response


@blp.route("/chatgptresponses")
class ChatGptResponseList(MethodView):
    @blp.response(200, ChatGptResponseSchema(many=True))
    def get(self):
        return ChatGptResponseModel.query.all()

    @blp.arguments(ChatGptResponseSchema)
    @blp.response(201, ChatGptResponseSchema)
    def post(self, response_data):
        response = ChatGptResponseModel(**response_data)

        try:
            db.session.add(response)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the Response.")

        return 