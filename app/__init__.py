from flask import Flask
from .extensions import db, bcrypt, login_manager, csrf
from .models import User
from .routes.auth_bp import auth_bp
from .routes.home_bp import home_bp
from .routes.errors_bp import errors_bp
from .routes.followers_bp import followers_bp

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.secret_key = 'thisisasecretkey'

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(errors_bp)
    app.register_blueprint(followers_bp)

    return app