from flask_restx import Resource
from app.main.util.dto import HealthDTO
import socket

namespace = HealthDTO.namespace


@namespace.route('/<random_string>')
@namespace.param('random_string', 'A random string')
class HelloRestAPI(Resource):

    @namespace.doc('Reserve String')
    def get(self, random_string):
        return "".join(reversed(random_string))

@namespace.route('/check')
class HealthAPI(Resource):

    __HOST_NAME = socket.gethostname()
    __HOST_IP = socket.gethostbyname(__HOST_NAME)

    @namespace.doc('Health')
    def get(self):

        response = {
            'status': 200,
            'host_name': HealthAPI.__HOST_NAME,
            'host_ip': HealthAPI.__HOST_IP,
            'message': 'UP'
        }
        return response, 200