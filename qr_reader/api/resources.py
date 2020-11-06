from flask import request
from flask_restful import Resource
import tempfile
import os
from .scan_ready import ReadyQR



class QR_Resource(Resource):
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp(prefix='qr_ready-prefix_')

    def get(self):
        return {'Error': 'Not Unique'}

    def post(self):
        image_file = request.files['file']
        temp_name = next(tempfile._get_candidate_names())
        file_path = os.path.join(self.temp_dir, temp_name)
        image_file.save(file_path)
        qr_r = ReadyQR(file_path)
        qr_code = qr_r.auto_find_qr_code()
        if qr_code :
            return(qr_code)
        else:
            return {'result': 'Not Identified'}

        # try:
        #     image_file = request.files['file']
        #     temp_name = next(tempfile._get_candidate_names())
        #     image_file.save(os.path.join(self.temp_dir, temp_name))
        #     return {'result': 'OK'}
        #
        # except:
        #     return {'Error': 'Not Unique'}

    def put(self):
        return {'Error': 'Not Unique'}
    def delete(self):
        return {'Error': 'Not Unique'}

 
