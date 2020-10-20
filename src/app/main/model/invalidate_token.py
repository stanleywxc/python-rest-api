from app.main import db
import datetime


class InvalidateToken(db.Model):

    """
    Token Model for storing JWT tokens
    """
    __tablename__   = 'invalid_tokens'

    id              = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token           = db.Column(db.String(500), unique=True, nullable=False)
    invalidated_on  = db.Column(db.DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.invalidated_on = datetime.datetime.now()

    def __repr__(self):
        return '<id: token: {}'.format(self.token)

    @staticmethod
    def check_invalidated(auth_token):
        # check whether auth token has been blacklisted
        res = InvalidateToken.query.filter_by(token=str(auth_token)).first()
        if res:
            return True
        else:
            return False
