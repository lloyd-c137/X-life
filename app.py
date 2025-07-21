from flask import Flask,g,session
import config
from utils import db
from flask_migrate import Migrate
from models import UserModel
from pack.view import view
from pack.auth import auth
from flask_cors import CORS

app = Flask(__name__)

app.config.from_object(config)
db.init_app(app)

migrate = Migrate(app,db)
app.register_blueprint(view)
app.register_blueprint(auth)
CORS(app)

@app.before_request
def load_user():
    user_id = session.get('id')
    if user_id:
        user = UserModel.query.get(user_id)
        setattr(g,'user',user)
    else:
        setattr(g,'user',None)


if __name__ == '__main__':
    app.run()
