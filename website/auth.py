from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Service_request,Service,Service_professional,Admin,Customer
from werkzeug.security import generate_password_hash, check_password_hash
from . import db   ##means from __init__.py import db
from werkzeug.utils import secure_filename
from flask_login import login_user,login_required,current_user,logout_user
import random

# Generate a random integer between a specified range
random_id = random.randint(1000, 9999)  # Example range


auth = Blueprint('auth', __name__)
@auth.route("/login",methods=['GET','POST'])
def login():
    if request.method=="POST":
        email=request.form.get("email")
        password=request.form.get("password")
        role=request.form.get("role")
        
        if role=="1":
            user=Admin.query.filter_by(email=email).first()
            if user:       
                if check_password_hash(user.password,password):
                    login_user(user,remember=True)
                    return redirect(url_for("views.admin"))
                else:
                    flash(message="Password or Email was incorrect!",category="error")
                    
        elif role=="2":
            user=Service_professional.query.filter_by(email=email).first()
            if user:
                if check_password_hash(user.password,password):
                    login_user(user,remember=True)
                    return redirect(url_for("views.service"))
                else:
                    flash(message="Password or Email was incorrect!",category="error")
            else:
                flash(message="Password or Email was incorrect!",category="error")
        else:
            user=Customer.query.filter_by(email=email).first()
            if user:
                if check_password_hash(user.password,password):
                    login_user(user,remember=True)
                    flash(message="Login was Successfull",category="success")
                    return redirect("/customer")
                else:
                    flash(message="Password or Email was incorrect!",category="error")
            else:
                flash(message="password or email was incorrect",category="error")

                           
    return render_template("login.html")

@auth.route("/signup",methods=['GET','POST'])
def signup():
    services=Service.query.all()
    if request.method=='POST':
        role=request.form.get('role')
        name=request.form.get('fullname')
        email=request.form.get('email')
        adress=request.form.get('adress')
        pincode=request.form.get('pincode')
        
        print(request.form)
        file=request.files["file"]
        filename=secure_filename(file.filename)
        fileData=file.read()
        description=request.form.get("description")
        service_name=request.form.get("service_name")
        password=request.form.get('password')
        experience=request.form.get("exp")
        id= random.randint(1000, 9999)
        service_id=db.session.query(Service.id).filter_by(name=service_name)
        if role=="2":
            customer= Customer(email=email,name=name,address=adress,pincode=pincode,password=generate_password_hash(password),id=id)
            db.session.add(customer)
            db.session.commit()
            login_user(customer,remember=True)
            return redirect(url_for("views.customer"))
        if role=="1":
            service_professional=Service_professional(email=email,name=name,address=adress,pincode=pincode,password=generate_password_hash(password),id=id,description=description,data=fileData, experience=experience,service_id=service_id)
            db.session.add(service_professional)
            db.session.commit()
            login_user(service_professional,remember=True)
            return redirect(url_for("views.admin"))     
            


    
    return render_template('sign_up.html',services=services)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))