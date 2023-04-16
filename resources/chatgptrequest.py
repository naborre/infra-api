from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import ChatGptRequestModel
from schemas import ChatGptRequestSchema


blp = Blueprint("ChatGptRequests", "chatgptrequests", description="Requests to ChatGPT")


@blp.route("/chatgptrequests/<int:request_id>")
class ChagGptRequest(MethodView):
    @jwt_required()
    @blp.response(200, ChatGptRequestSchema)
    def get(self, request_id):
        request = ChatGptRequestModel.query.get_or_404(request_id)
        return request
    
    @jwt_required()
    def delete(self, request_id):
        request = ChatGptRequestModel.query.get_or_404(request_id)
        db.session.delete(request)
        db.session.commit()
        return {"message": "Request deleted"}, 200


@blp.route("/chatgptrequests")
class ChagGptRequestList(MethodView):
    @jwt_required()
    @blp.response(200, ChatGptRequestSchema(many=True))
    def get(self):
        return ChatGptRequestModel.query.all()

    @jwt_required()
    @blp.arguments(ChatGptRequestSchema)
    @blp.response(201, ChatGptRequestSchema)
    def post(self, request_data):
        request = ChatGptRequestModel(**request_data)
        try:
            db.session.add(request)
            db.session.commit()
        except IntegrityError:
            abort(
                400,
                message="Request already exists.",
            )
        except SQLAlchemyError:
            abort(500, message="An error occurred creating the Request.")

        return 