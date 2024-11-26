
from sqlalchemy.sql import func
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime 
db = SQLAlchemy()
from datetime import datetime
DB_NAME = "database.db"
from sqlalchemy.orm import relationship
class Admin(db.Model,UserMixin):
    __tablename__ = "admin"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email=db.Column(db.String(80),unique=True)
    password=db.Column(db.String(200))
     

class Customer(db.Model,UserMixin):
    __tablename__ = "customer"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String, nullable=False)
    address=db.Column(db.String(80),nullable=False)
    pincode=db.Column(db.Integer,nullable=False)
    phone=db.Column(db.Integer)
    service_requested=db.relationship('Service_request')
    

class Service_request(db.Model):
    __tablename__ = "service_request"

    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer,db.ForeignKey("service.id"))
    customer_id = db.Column(db.Integer,db.ForeignKey("customer.id"))
    date_requested=db.Column(db.DateTime(timezone=True),default=datetime.now())
    date_completed=db.Column(db.DateTime(timezone=True))
    service_status=db.Column(db.String,default="pending")
    professional_id=db.Column(db.Integer,db.ForeignKey("service_professional.id"))

class Service_professional(db.Model,UserMixin):
    __tablename__ = "service_professional"

    id = db.Column(db.Integer, primary_key=True)
    service_id=db.Column(db.Integer,db.ForeignKey('service.id'))
    email = db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    experience=db.Column(db.Integer)
    data = db.Column(db.LargeBinary)
    password = db.Column(db.String, nullable=False)
    date_created=db.Column(db.DateTime(),default=datetime.now())
    description = db.Column(db.String, nullable=False)
    address=db.Column(db.String(80),nullable=False)
    pincode=db.Column(db.Integer,nullable=False)
    verification_status=db.Column(db.String,default="pending")
    service_requests = db.relationship('Service_request', secondary="prof_req")
    


class Service(db.Model):
    __tablename__ = "service"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String, nullable=False)
    base_price=db.Column(db.Integer,nullable=False)
    service_professional=db.relationship('Service_professional')

class Reviews(db.Model):
    __tablename__="reviews"
    id=db.Column(db.Integer,primary_key=True)
    prof_id=db.Column(db.Integer,db.ForeignKey("service_professional.id"))
    customer_id=db.Column(db.Integer,db.ForeignKey("customer.id"))
    rating=db.Column(db.Integer,nullable=False)
    description=db.Column(db.String)

class Prof_req(db.Model):
    __tablename__="prof_req"
    prof_id=db.Column(db.Integer,db.ForeignKey("service_professional.id"),primary_key=True)
    req_id=db.Column(db.Integer,db.ForeignKey("service_request.id"))