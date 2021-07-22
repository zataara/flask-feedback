from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
        db.app = app
        db.init_app(app)

## Model is used as a placefiller reference. Make sure to change all 'Model' instances to a variable of your chooseing.

class Model(db.Model):
    '''Database model for Models'''

    __tablename__ = 'Model'

    def __repr__(self):
        
        u = self
        return f'<Model {u.id} '

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    

