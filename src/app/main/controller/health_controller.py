from flask_restx import Resource
from app.main.util.dto import HealthDTO

namespace = HealthDTO.namespace


@namespace.route('/<random_string>')
@namespace.param('random_string', 'A random string')
class HelloRestAPI(Resource):

    @namespace.doc('Reserve String')
    def get(self, random_string):
        return "".join(reversed(random_string))

@namespace.route('/check')
class HealthAPI(Resource):

    @namespace.doc('Health')
    def get(self):

        response = {
            'status': 200,
            'message': 'UP'
        }
        return response, 200