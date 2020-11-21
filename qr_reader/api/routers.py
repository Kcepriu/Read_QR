from flask import Blueprint
from flask_restful import Api

from .resources import QR_Info_Resource, Files_Resource

api_app = Blueprint('api', __name__)

api = Api(api_app)

api.add_resource(QR_Info_Resource,  '/qr_info',    '/qr_info/<id_document>')
api.add_resource(Files_Resource,    '/get_files/<id_document>')
