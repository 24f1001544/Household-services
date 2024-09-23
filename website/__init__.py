from flask import Flask
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
    
    # def add_services():
    #     services=[
    #     {"id": 1, "name": "House Cleaning", "price": 1500, "description": "Comprehensive house cleaning services."},
    #     {"id": 2, "name": "Plumbing Services", "price": 500, "description": "Expert plumbing services."},
    #     {"id": 3, "name": "Electrician Services", "price": 600, "description": "Electrical repair and installation."},
    #     {"id": 4, "name": "Pest Control", "price": 2000, "description": "Effective pest control solutions."},
    #     {"id": 5, "name": "Appliance Repair", "price": 800, "description": "Repair services for home appliances."},
    #     {"id": 6, "name": "Painting Services", "price": 20 , "description": "Interior and exterior painting services."},
    #     {"id": 7, "name": "Furniture Assembly", "price": 1000, "description": "Assembly services for furniture."},
    #     {"id": 8, "name": "AC Maintenance", "price": 1500, "description": "Air conditioner cleaning and maintenance."},
    #     {"id": 9, "name": "Gardening Services", "price": 1200, "description": "Garden maintenance services."},
    #     {"id": 10, "name": "Home Deep Cleaning", "price": 3000, "description": "Deep cleaning services for your home."} ]

    #     for service in services:
    #        new_service = Service(id=service["id"], name=service["name"], base_price=service["price"], description=service["description"])
    #        db.session.add(new_service)

    #        db.session.commit()

# Call the function to add services to the database

    with app.app_context():
        
        db.create_all()

    # login_manager = LoginManager()
    # login_manager.login_view = 'auth.login'
    # login_manager.init_app(app)

   

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
