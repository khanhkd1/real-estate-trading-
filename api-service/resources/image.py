from flask_restful import Resource
from flask import request
import requests
from requests.exceptions import RequestException
from base64 import b64encode
from flask_jwt_extended import jwt_required
from config import IMGUR_TOKEN, ALLOWED_FILES, SIZE_FILE_MAX


class ImageApi(Resource):
    @jwt_required()
    def post(self):
        img_urls = []
        for key in request.files.keys():
            if allowed_file(request.files[key].filename):
                file = request.files[key].read()
                if len(file) <= SIZE_FILE_MAX:
                    try:
                        img_urls.append(requests.post(
                            'https://api.imgur.com/3/image',
                            headers={'Authorization': f'Bearer {IMGUR_TOKEN}'},
                            data={
                                'image': b64encode(file),
                                'type': 'base64'
                            }
                        ).json()['data']['link'])
                    except RequestException:
                        continue
        return {'images': img_urls}, 200


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_FILES
