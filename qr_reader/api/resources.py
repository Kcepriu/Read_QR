from flask import request
from flask_restful import Resource

class QR_Resource(Resource):
    def get(self, id_files):
        if id_files:
            # obj = User.objects.get(id=id_user)
            # return UsersSchema().dump(obj)
            pass

    def post(self):
        # try:
        #     res = UsersSchema().load(request.get_json())
        #     obj = User.objects.create(**res)
        #     return UsersSchema().dump(obj)
        # except ValidationError as err:
        #     return {'error': err.messages}
        # except NotUniqueError:
        #     return {'Error': 'Not Unique'}
        pass

    def put(self):
        return {'Error': 'Not Unique'}
    def delete(self):
        return {'Error': 'Not Unique'}

 
