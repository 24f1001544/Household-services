
from sqlalchemy.sql import func
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
DB_NAME = "database.db"

class Admin(db.Model,UserMixin):
    __tablename__ = "admin"

    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email=db.Column(db.String(80),unique=True)
    password=db.Column(db.String(200))
  

class Customer(db.Model,UserMixin):
    __tablename__ = "customer"

    id = db.Column(db.String, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String, nullable=False)
    address=db.Column(db.String(80),nullable=False)
    pincode=db.Column(db.Integer,nullable=False)
    service_requested=db.relationship('Service_request')

class Service_request(db.Model):
    __tablename__ = "service_request"

    id = db.Column(db.String, primary_key=True)
    service_id = db.Column(db.Integer,db.ForeignKey("service.id"))
    customer_id = db.Column(db.Integer,db.ForeignKey("customer.id"))
    professional_id = db.Column(db.Integer,db.ForeignKey("service_professional.id"))
    date_requested=db.Column(db.DateTime(timezone=True),default=func.now())
    date_completed=db.Column(db.DateTime(timezone=True))
    service_status=db.Column(db.String)

class Service_professional(db.Model,UserMixin):
    __tablename__ = "service_professional"

    id = db.Column(db.String, primary_key=True)
    service_id=db.Column(db.Integer,db.ForeignKey('service.id'))
    email = db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    service_name = db.Column(db.String(80), nullable=False)
    experience=db.Column(db.Integer)
    data = db.Column(db.LargeBinary)
    password = db.Column(db.String, nullable=False)
    date_created=db.Column(db.DateTime(timezone=True),default=func.now())
    description = db.Column(db.String, nullable=False)
    address=db.Column(db.String(80),nullable=False)
    pincode=db.Column(db.Integer,nullable=False)
    service_request=db.relationship("Service_request")


class Service(db.Model):
    __tablename__ = "service"

    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String, nullable=False)
    base_price=db.Column(db.Integer,nullable=False)
    service_professional=db.relationship('Service_professional')
