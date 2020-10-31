from flask import Blueprint
from flask_restful import Api

from .resources import QR_Resource

api_app = Blueprint('api', __name__)

api = Api(api_app)

api.add_resource(QR_Resource,  '/qr',    '/qr/<id_files>')
