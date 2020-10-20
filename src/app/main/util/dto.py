from flask_restx import Namespace, fields


class UserDTO:
    namespace = Namespace('user', description='user related operations')
    user = namespace.model('user', {
        'email': fields.String(required=True, description='user email address'),
        'username': fields.String(required=True, description='user username'),
        'password': fields.String(required=True, description='user password'),
        'public_id': fields.String(description='user Identifier')
    })


class AuthDTO:
    namespace = Namespace('auth', description='authentication related operations')
    user_auth = namespace.model('auth_details', {
        'email': fields.String(required=True, description='The email address'),
        'password': fields.String(required=True, description='The user password '),
    })

class HealthDTO:
    namespace = Namespace('health', description='health endpoints')