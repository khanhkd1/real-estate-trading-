from flask_restful import Resource
from flask import request
import requests
from requests.exceptions import RequestException
from base64 import b64encode
from flask_jwt_extended import jwt_required
from config import IMGUR_TOKEN


class ImageApi(Resource):
    @jwt_required()
    def post(self):
        img_urls = []
        for key in request.files.keys():
            try:
                img_urls.append(requests.post(
                    'https://api.imgur.com/3/image',
                    headers={'Authorization': f'Bearer {IMGUR_TOKEN}'},
                    data={
                        'image': b64encode(request.files[key].read()),
                        'type': 'base64'
                    }
                ).json()['data']['link'])
            except RequestException as e:
                pass
        return img_urls
