from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import ChatGptRequestModel, ChatGptResponseModel
from schemas import ChatGptRequestSchema
import sys
import openai


blp = Blueprint("ChatGptRequests", "chatgptrequests", description="Requests to ChatGPT")

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0.5,
    )
    return response.choices[0].message["content"]


@blp.route("/chatgptrequests")
class ChatGptRequest(MethodView):
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
            
        Cob1 = """Daños Materiales Parciales - POL120160325
        cobertura de indemnización por daños materiales directos a un vehículo asegurado en los siguientes casos:  \
        volcamiento o colisión accidental con objetos en movimiento o estacionarios, incendio, rayo o explosión, ya sea  \
        que el vehículo esté estacionado o en movimiento. También incluye los daños causados durante el traslado del vehículo  \
        asegurado por grúa o por un servicio de transporte permitido por la autoridad competente."""

        Cob2 = """Responsabilidad Civil - POL120160325
        Cobertura implica que la aseguradora indemnizará al tercero inocente perjudicado según las condiciones de  \
        la subsección contratada, siempre y cuando la responsabilidad civil del asegurado sea declarada por sentencia  \
        ejecutoriada. La aseguradora pagará la indemnización al tercero inocente perjudicado en virtud de sentencia  \
        ejecutoriada o de transacción judicial o extrajudicial"""
        
        relato = request.request
        
        prompt = f"""
        En base a la siguiente informacion acerca de polizas de seguro, identifica cuales serian las aplicables \
        al texto enmarcado en <>. 

        Informacion Polizas de seguro con 2 coberturas:
        {Cob1}  
        {Cob2}

        relato:
        <{relato}>

        considera que es posible que se aplique solo 1 cobertura, ambas o ninguna.
        """

        try:
            response_text = get_completion(prompt)
            response = ChatGptResponseModel(request_id=request.id, response=response_text)
        except Exception as e:
            print(e, file=sys.stderr)

        try:
            db.session.add(response)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            abort(500, message="An error occurred while inserting the Response.")

        return response.response

