from app.main import db
from app.main.model.invalidate_token import InvalidateToken


class InvalidateTokenService:

    @staticmethod
    def invalidate(token):
        invalidated_token = InvalidateToken(token=token)
        try:
            # insert the token
            db.session.add(invalidated_token)
            db.session.commit()
            response_object = {
                'status': 'success',
                'message': 'Successfully logged out.'
            }
            return response_object, 200
        except Exception as e:
            response_object = {
                'status': 'fail',
                'message': str(e)
            }
            return response_object, 200
