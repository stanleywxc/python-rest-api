from flask import request
from flask_restx import Resource

from app.main.service.auth_service import AuthenticationService
from app.main.util.dto import AuthDTO

namespace = AuthDTO.namespace
user_auth = AuthDTO.user_auth


@namespace.route('/login')
class LoginAPI(Resource):
    """
        User Login Resource
    """
    @namespace.doc('user login')
    @namespace.expect(user_auth, validate=True)
    def post(self):
        # get the post data
        post_data = request.json
        return AuthenticationService.login_user(data=post_data)


@namespace.route('/logout')
class LogoutAPI(Resource):
    """
    Logout Resource
    """
    @namespace.doc('logout a user')
    def post(self):
        # get auth token
        auth_header = request.headers.get('Authorization')
        return AuthenticationService.logout_user(data=auth_header)
