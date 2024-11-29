from flask import Flask,request,session
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from .models import db,DB_NAME


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import Admin,Service,Service_professional,Service_request,Customer
   
    with app.app_context():
        db.create_all()
        
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    

    @login_manager.user_loader
    def load_user(user_id):
    # Get user type from session
        user_type = session.get('user_type')  # Ensure the key is a string

    # Load the user based on the type
        if user_type == "customer":
            return Customer.query.get(int(user_id))
        elif user_type == "service":
           return Service_professional.query.get(int(user_id))
        elif user_type == "admin":
           return Admin.query.get(int(user_id))
        return None  # Return None if user type is not recognized
    return app


def create_database(app): 
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
