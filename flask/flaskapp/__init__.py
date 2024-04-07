import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS, cross_origin
from flask_jwt_extended import JWTManager
from datetime import timedelta
from .verification import init_mail

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    cors = CORS(app)
    jwt = JWTManager(app)

    app.config['CORS_HEADER'] = 'Content-Type'

    # TODO: Replace placeholder secret key
    app.config['JWT_SECRET_KEY'] = 'super-secret'
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)

    app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
    db_pass = os.environ['POSTGRES_PASSWORD']
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://postgres:{db_pass}@postgres:5432/main'

    # Initialize Flask-Mail
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = 'ragur@ualberta.ca'
    app.config['MAIL_PASSWORD'] = 'nujden-currup-8Cavse'
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_DEFAULT_SENDER'] = 'ragur@ualberta.ca'
    app.config['BASE_URL'] = 'https://localhost/api'

    init_mail(app)

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
    app.register_blueprint(auth_blueprint, url_prefix='/api')

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint, url_prefix='/api')

    return app