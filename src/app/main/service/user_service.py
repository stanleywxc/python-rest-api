import uuid
import datetime

from app.main import db
from app.main.model.user import User


class UserService:

    @staticmethod
    def save_new_user(data):
        user = User.query.filter_by(email=data['email']).first()
        if not user:
            new_user = User(
                public_id=str(uuid.uuid4()),
                email=data['email'],
                username=data['username'],
                password=data['password'],
                registered_on=datetime.datetime.utcnow()
            )

            UserService.save_changes(new_user)

            return UserService.generate_token(new_user)
        else:
            response_object = {
                'status': 'fail',
                'message': 'User already exists. Please Log in.',
            }
            return response_object, 409

    @staticmethod
    def get_all_users():
        return User.query.all()

    @staticmethod
    def get_a_user(public_id):
        return User.query.filter_by(public_id=public_id).first()

    @staticmethod
    def save_changes(data):
        db.session.add(data)
        db.session.commit()

    @staticmethod
    def generate_token(user):
        try:
            # generate the auth token
            auth_token = user.encode_auth_token()
            response_object = {
                'status': 'success',
                'message': 'Successfully registered.',
                'Authorization': auth_token.decode()
            }
            return response_object, 201
        except Exception as e:
            response_object = {
                'status': 'fail',
                'message': str(e)
            }
            return response_object, 401
