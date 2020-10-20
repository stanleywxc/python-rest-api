# app/__init__.py

from flask_restx import Api
from flask import Blueprint

from app.main.controller.user_controller import namespace as user_ns
from app.main.controller.auth_controller import namespace as auth_ns
from app.main.controller.health_controller import namespace as health_ns


blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='REST API WITH JWT',
          version='1.0',
          description='Rest API Web Services'
          )

api.add_namespace(user_ns, path='/user')
api.add_namespace(auth_ns, path='/auth')
api.add_namespace(health_ns, path='/health')
