import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
    db_pass = os.environ['POSTGRES_PASSWORD']
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://postgres:{db_pass}@postgres:5432/main'

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(userid):
        query = db.text('SELECT * FROM kkuser WHERE UserID = :userid')

        result = db.session.execute(query, {'userid': userid})

        user = result.fetchone()

        if not user:
            return
        else:
            return User(user)
        

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app