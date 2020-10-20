from flask import request
from flask_restx import Resource

from app.main.util.dto import UserDTO
from app.main.service.user_service import UserService

namespace = UserDTO.namespace
_user = UserDTO.user


@namespace.route('/')
class UserList(Resource):

    @namespace.doc('list_of_registered_users')
    @namespace.marshal_list_with(_user, envelope='data')
    def get(self):
        """List all registered users"""
        return UserService.get_all_users()

    @namespace.response(201, 'User successfully created.')
    @namespace.doc('create a new user')
    @namespace.expect(_user, validate=True)
    def post(self):
        """Creates a new User """
        data = request.json
        return UserService.save_new_user(data=data)


@namespace.route('/<public_id>')
@namespace.param('public_id', 'The User identifier')
@namespace.response(404, 'User not found.')
class User(Resource):

    @namespace.doc('get a user')
    @namespace.marshal_with(_user)
    def get(self, public_id):
        """get a user given its identifier"""
        user = UserService.get_a_user(public_id)
        if not user:
            namespace.abort(404)
        else:
            return user
