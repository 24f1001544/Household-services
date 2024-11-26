from flask import Blueprint, render_template, request, flash, jsonify, url_for,redirect
from flask_login import login_required, current_user
from .models import Service,Service_request,Service_professional,Customer
from . import db
from datetime import datetime
from flask_login import login_user,login_required,current_user,logout_user

views = Blueprint('views', __name__)


@views.route("/")
@login_required
def home():
    return render_template("customer.html")

@views.route("/admin")
@login_required
def admin():
    services=Service.query.all()
    profs=db.session.query(
        Service.name.label("service_name"),
        Service_professional.id.label("id"),
        Service_professional.name.label("name"),
        Service_professional.experience.label("experience"),
        Service_professional.verification_status.label("status")
    ).join(Service,Service_professional.service_id==Service.id)\
    .filter(Service.id==Service_professional.service_id).all()
    prof=profs[0]
    print(prof.status)
    reqs=Service_request.query.all()
    return render_template("home.html",services=services,profs=profs,reqs=reqs)
# reject or accept service professional
@views.route("/admin/<int:id>",methods=["POST"])
def prof(id):
    request_type=request.form.get("action")
    if request_type=="accept":
        prof=Service_professional.query.get(id)
        prof.verification_status="verified"
        db.session.commit()
        return redirect("/",flash(message="Password or Email was incorrect!",category="error"))
    elif request_type=="reject":
        prof=Service_professional.query.get(id)
        db.session.delete(prof)
        db.session.commit()
        return redirect("/admin")
    else:
        prof=Service_professional.query.get(id)
        db.session.delete(prof)
        db.session.commit()
        return redirect("/admin",flash(message="Service Professional Deleted Succesfully",category="success"))
    


# customer route
@views.route("/customer")
@login_required
def customer():
    
    services=Service.query.all()
    
    customer_id = current_user.id  # Get the customer ID from the current user object

    # Query to get service requests associated with the current customer
    service_history = db.session.query(
        Service_request.id.label('request_id'),  # Service Request ID
        Service_request.service_status.label('status'),  # Status of the request
        Service.name.label('name'),  # Professional's name
        Service_request.date_requested.label("date_created"),
        Service_request.date_completed.label("date_completed")
    ).join(Service, Service_request.service_id == Service.id) \
    .filter(Service_request.customer_id == current_user.id).all()
    
    
    return render_template("customer.html",services=services,service_history=service_history)

# service professional route
@views.route("/service")
@login_required
def service():
    
    user=Service_professional.query.filter_by(id=int(current_user.id)).first()
    service_request= db.session.query(
       Customer.name.label("name"),
       Customer.address.label("address"),
       Customer.pincode.label("pincode"),
       Customer.phone.label("phone"),
       Service_request.id.label("id"),
       Service_request.service_status.label("status")
    ).join(Service_request, Service_request.customer_id == Customer.id) \
    .filter(Service_request.service_id == user.service_id).all()
    print(service_request)
    return render_template("service_professional.html",user=user,service_request=service_request)



@views.route("/customer/request/<int:service_id>",methods=["GET","POST"])
def add_service(service_id ):
    if request.method=="POST":
        print(current_user)
        newService_request=Service_request(service_id=service_id,customer_id=int(current_user.id))
        db.session.add(newService_request)
        db.session.commit()
        return redirect(url_for("views.customer"))
    else:
      
      service= Service.query.get(service_id)
      services=Service_professional.query.filter_by(service_id=service.id)
      customer_id=current_user.id
    return render_template("new_request.html",service=service,customer_id=customer_id,services=services)

@views.route("customer/service_request/<int:request_id>",methods=["POST","GET"])
def close_service(request_id):
    query = (
    db.session.query(
        Service_request.id.label("service_request_id"),
        Service_request.customer_id,
        Service_request.date_requested,
        Service.name.label("service_name"),
        Service.description.label("service_description"),
    )
    .join(Service, Service_request.service_id == Service.id)
    .filter(Service_request.id == request_id)  # Replace with actual ID
    )
    # service_request=service_request1.join(Service).filter(service_request1.service_id == Service.id)
    # print(service_request)
    return render_template("review.html",service_request=query.first())
@views.route("service/<int:service_id>",methods=["POST"])
def accept_reject_service(service_id):
    request_type=request.form.get("form_type")
    service_request=Service_request.query.get(service_id)
    print(request_type)
    if request_type=="accept":
        service_request.professional_id=int(current_user.id)
        service_request.service_status="accepted"
        print(service_request)
        db.session.commit()
        flash(message="Request Accepted Successfully",category="success")
        return redirect("/service")
    elif request_type=="reject":
        service_request.professional_id=None
        service_request.service_status="pending"
        db.session.commit()
        flash(message="Request Rejected Successfully",category="success")
        return redirect("/service")
    else:
        return redirect("/service",flash(message="Request Closed Successfully",category="success"))
        
@views.route("/dashboard")
def dashboard():
    print(Service_professional.service_requests)
    return render_template("dashboard.html")

@views.route("/edit/<int:service_id>",methods=["GET","POST"])
def editService(service_id):
      service=Service.query.filter_by(id=service_id).first()
      if request.method=="GET":
        
        print(service.description)
        return render_template("edit_service.html",service=service)
      else:
          name=request.form.get("name")
          description=request.form.get("description")
          base_price=request.form.get("base_price")
          service.name=name
          service.description=description
          service.base_price=base_price
          db.session.commit()
          return redirect("/")
      
@views.route("/delete/<int:service_id>",methods=["POST"])
def delete_service(service_id):
    service=Service.query.filter_by(id=service_id).first()
    db.session.delete(service)
    db.session.commit()
    return redirect("/")

@views.route("/newService",methods=["GET","POST"])
def newService():
    if request.method=="GET":
        return render_template("newService.html")
    else:
        name=request.form.get("name")
        description=request.form.get("description")
        base_price=request.form.get("base_price")
        service=Service(name=name,description=description,base_price=base_price)
        db.session.add(service)
        db.session.commit()
        return redirect("/")

@views.route('/customer/search', methods=['GET'])
def search():
    search_by = request.args.get('search_by', '')  # The selected option
    search_term = request.args.get('search_term', '')  # The user input for search term

    # Base query
    query = Service.query

    # Apply the selected filter
    if search_by == 'name' and search_term:
        query = query.filter(Service.name.ilike(f'%{search_term}%'))
    elif search_by == 'location' and search_term:
        query = query.filter(Service_professional.pincode.ilike(f'%{search_term}%'))
    # elif search_by == 'date' and search_term:
    #     try:
    #         search_date = datetime.strptime(search_term, '%Y-%m-%d').date()
    #         query = query.filter(.date == search_date)
    #     except ValueError:
    #         return "Invalid date format. Use YYYY-MM-DD.", 400

    results = query.all()
    return render_template('customer_search.html', results=results, search_by=search_by, search_term=search_term)
