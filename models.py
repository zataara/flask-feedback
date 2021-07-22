from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

def connect_db(app):
        db.app = app
        db.init_app(app)

## Model is used as a placefiller reference. Make sure to change all 'Model' instances to a variable of your chooseing.

class User(db.Model):
    '''Database model for Models'''

    __tablename__ = 'users'

    def __repr__(self):
        
        u = self
        return f'<User {u.id} >'

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    username = db.Column(db.String(20),
                            nullable=False,
                            unique=True)
    password = db.Column(db.String,
                            nullable=False)
    email = db.Column(db.String(50),
                            nullable=False)
    first_name = db.Column(db.String(30),
                            nullable=False)
    last_name = db.Column(db.String(30),
                            nullable=False)
    

