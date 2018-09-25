import datetime
from webapp import db, bcrypt
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

class User(db.Model):

    __tablename__ = "users"

    #insert info to the column
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, email, password, admin):
        logger("User constructor")
        self.email = email
        self.password = password
        self.admin = admin

    def is_authenticated(self):
        logger("is_authenticated")
        return True

    def is_active(self):
        logger("is_active function")
        return True

    def is_anonymous(self):
        logger("is_anonymous function")
        return False

    def get_id(self):
        logger("get_id function")
        return self.id
    def __repr__(self):
        return '<User {0}>'.format(self.email)