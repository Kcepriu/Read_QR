from flask import Response, abort
from flask_restful import Resource
from mongoengine.errors import ValidationError, OperationError
import json

from ..db import ScanDocument
from .schemas import QR_Schema
from ..bot import bot_instance

class Files_Resource(Resource):
    def get(self, id_document):
        try:
            obj = ScanDocument.objects.get(id=id_document)
        except ValidationError:
            abort(404)

        mimetype = obj.mime_type
        content = obj.data_file.read()

        resp = Response(content, mimetype=mimetype)
        return resp

    def post(self):
        return {'Error': 'Not Unique'}

    def put(self, id_document):
        try:
            obj = ScanDocument.objects.get(id=id_document)
        except ValidationError:
            abort(404)

        if not obj.data_file:
            if not bot_instance.get_url_file(obj):
                return {'status': 'ERROR'}

        if obj.get_qr_cod():
            return {'status': 'OK'}
        else:
            return {'status': 'ERROR'}


    def delete(self, id_document):
        try:
            obj = ScanDocument.objects.get(id=id_document)
        except ValidationError:
            abort(404)

        try:
            obj.delete()
        except OperationError as err:
            return {'error': err.messages}

        return {'status': 'OK'}


class QR_Info_Resource(Resource):
    def get(self, id_document=None):
        if id_document:
            try:
                obj = ScanDocument.objects(id=id_document).get()
                dump_obj = QR_Schema().dump(obj)
            except ValidationError:
                abort(404)
        else:
            obj = ScanDocument.objects()
            dump_obj = QR_Schema().dump(obj, many=True)

        r = Response(response=json.dumps(dump_obj, ensure_ascii=False), status=200, mimetype="application/json")
        r.headers["Content-Type"] = "application/json; charset=utf-8"
        return r

    def post(self):
        return {'Error': 'Not Unique'}

    def put(self):
        return {'Error': 'Not Unique'}

    def delete(self):
        return {'Error': 'Not Unique'}

 
