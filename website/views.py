from flask import Blueprint, render_template, request, flash, jsonify, url_for,redirect,abort,session,send_file
from flask_login import login_required, current_user
from .models import Service,Service_request,Service_professional,Customer,Reviews
from . import db
from datetime import datetime
from flask_login import login_user,login_required,current_user,logout_user
from io import BytesIO
views = Blueprint('views', __name__)
from sqlalchemy import func

import functools

def role_required(required_role):
    def decorator(func):
        @functools.wraps(func)
        @login_required
        def wrapper(*args, **kwargs):
            if session.get('user_type') != required_role:
                abort(403)
            return func(*args, **kwargs)
        return wrapper
    return decorator

@views.route("/")
@login_required
def home():
    return render_template("customer.html")

@views.route("/admin")
@role_required("admin")
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
    reqs=Service_request.query.all()
    return render_template("home.html",services=services,profs=profs,reqs=reqs)
# reject or accept service professional
@views.route("/admin/<int:id>",methods=["POST"])
@role_required("admin")
def prof(id):
    request_type=request.form.get("action")
    if request_type=="accept":
        prof=Service_professional.query.get(id)
        prof.verification_status="verified"
        db.session.commit()
        flash(message="Professional Verified Successfully",category="success")
        return redirect("/admin")
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
@role_required("customer")
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
@role_required("service")
def service():
    user=Service_professional.query.filter_by(id=int(current_user.id)).first()
    service_request= db.session.query(
       Customer.name.label("name"),
       Customer.address.label("address"),
       Customer.pincode.label("pincode"),
       Customer.phone.label("phone"),
       Service_request.id.label("id"),
       Service_request.service_status.label("status"),
       Service_request.date_requested.label("date_created"),
       Service_request.date_completed.label("date_completed"),
       Service_request.professional_id.label("prof_id")
    ).join(Service_request, Service_request.customer_id == Customer.id) \
    .filter(Service_request.service_id == user.service_id).all()
    return render_template("service_professional.html",user=user,service_request=service_request)



@views.route("/customer/request/<int:service_id>",methods=["GET","POST"])
@role_required("customer")
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
@role_required("customer")
def close_service(request_id):
    service_request=Service_request.query.filter_by(id=request_id).first()
    if request.method == 'POST':
        # Get review data from the form
        rating = request.form.get('review[rating]')
        comment = request.form.get('review[comment]')
        
        # Assuming the professional_id is part of the service request
        professional_id = service_request.professional_id
        
        # Create a new Review entry
        review = Reviews(
            customer_id=current_user.id,
            prof_id=professional_id,
            rating=int(rating),
            description=comment
        )
        service_request.service_status="closed"
        # Add the review to the database
        db.session.add(review)
        db.session.commit()

        flash("Review submitted successfully!", "success")
        return redirect("/customer")
    
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
@role_required("service")
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
@login_required
def dashboard():
    counts = (
        db.session.query(Service_request.service_status, func.count(Service_request.id))
        .filter(Service_request.customer_id == int(current_user.id))
        .group_by(Service_request.service_status)
        .all()
    )
    count_dict = {status: count for status, count in counts}
    for key in ['closed', 'pending','accepted']:
        count_dict.setdefault(key, 0)
    
   
    print(count_dict)
    
    return render_template("dashboard.html",count_dict=count_dict)

@views.route("/edit/<int:service_id>",methods=["GET","POST"])
@role_required("admin")
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
          return redirect("/admin")
      
@views.route("/delete/<int:service_id>",methods=["POST"])
@role_required("admin")
def delete_service(service_id):
    service=Service.query.filter_by(id=service_id).first()
    db.session.delete(service)
    db.session.commit()
    return redirect("/")

@views.route("/newService",methods=["GET","POST"])
@role_required("admin")
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
        return redirect("/admin")

@views.route('/customer/search', methods=['GET'])
@role_required("customer")
def search():
    search_by = request.args.get('search_by', '')  # The selected option
    search_term = request.args.get('search_term', '')  # The user input for search term
    results = []
    # Base query
    query=Service_professional.query.join(Service).filter(Service.id==Service_professional.service_id)


    # Apply the selected filter
    if search_by == 'name' and search_term:
        query = query.filter(Service.name.ilike(f'%{search_term}%'))
    elif search_by == 'location' and search_term:
        query = query.filter(Service_professional.address.ilike(f'%{search_term}%'))
    elif search_by == 'pincode' and search_term:
        query = query.filter(Service_professional.pincode == search_term)
    results = query.all()


    query1 = Service_request.query.join(Service_professional).filter(Service_request.customer_id == int(current_user.id))
    if search_by == 'name' and search_term:
        query1 = query1.filter(Service_professional.description.ilike(f'%{search_term}%'))
    elif search_by == 'location' and search_term:
        query1 = query1.filter(Service_professional.address.ilike(f'%{search_term}%'))
    elif search_by == 'pincode' and search_term:
        query1 = query1.filter(Service_professional.pincode == search_term)
    results1 = query1.all()
    # print(results1[0].professional.description)
    # for request in professional.service_requests:
    #     print(request.service.name, request.service_status)
    return render_template('customer_search.html', results=results, search_by=search_by, search_term=search_term,results1=results1)

@views.route('/service/search', methods=['GET'])
@role_required("service")
def search_service():
    search_by = request.args.get('search_by', '')  # The selected option
    search_term = request.args.get('search_term', '')  # The user input for search term
    
    # Base query
    query=Customer.query.join(Service_request).filter(Customer.id==Service_request.customer_id and int(current_user.id)==Service_request.professional_id)


    # Apply the selected filter
    if search_by == 'name' and search_term:
        query = query.filter(Customer.name.ilike(f'%{search_term}%'))
    elif search_by == 'location' and search_term:
        query = query.filter(Customer.address.ilike(f'%{search_term}%'))
    elif search_by == 'pincode' and search_term:
        query = query.filter(Customer.pincode == search_term)
    results = query.all()
    for service in results:
        for req in service.service_requested:
            print(req)
    return render_template('service_search.html', results=results, search_by=search_by, search_term=search_term)

@views.route('admin/viewprof/<int:prof_id>')
def view_prof(prof_id):
    service_prof = Service_professional.query.get_or_404(prof_id)
    reviews=Reviews.query.filter_by(prof_id=prof_id)
    return render_template('viewProf.html', service_prof=service_prof,reviews=reviews)

@views.route('admin/viewprof/serve_pdf/<int:prof_id>')
def serve_data(prof_id):
    service_prof = Service_professional.query.get_or_404(prof_id)
    if service_prof.data:
        return send_file(
            BytesIO(service_prof.data),
            mimetype='application/pdf',
            as_attachment=True,  # If you want the browser to download it
            download_name=f"{service_prof.name}_profile.pdf"  # Customize the filename
        )
    return "No photo available", 404

@views.route("/customer/profile")
@role_required("customer")
def customer_profile():
    customer=Customer.query.get(int(current_user.id))
    return render_template("customer_profile.html",customer=customer)

@views.route("/customer/profile/edit",methods=["GET","POST"])
@role_required("customer")
def customer_profile_edit():
    customer=Customer.query.get(int(current_user.id))
    if request.method=="GET":
       
       return render_template("customer_profile_edit.html",customer=customer)
    elif request.method=="POST":
        customer.name=request.form.get("name")
        customer.email=request.form.get("email")
        customer.address=request.form.get("address")
        customer.pincode=request.form.get("pincode")
        customer.phone=request.form.get("phone")
        db.session.commit()
        flash(message="Details Updated Successfully",category="success")
        return redirect("/customer")
    
@views.route("/service/profile")
@role_required("service")
def service_profile():
    service_prof=Service_professional.query.get(int(current_user.id))
    return render_template("service_profile.html",service_prof=service_prof)

@views.route("service/profile/edit",methods=["GET","POST"])
@role_required("service")
def service_profile_edit():
    service_prof=Service_professional.query.get(int(current_user.id))
    if request.method=="GET":
        services=Service.query.all()
        return render_template("service_profile_edit.html",service_prof=service_prof,services=services)
    elif request.method=="POST":
       service_name=request.form.get("service_name")
       service_prof.name=request.form.get("name")
       service_prof.email=request.form.get("email")
       service_prof.experience=request.form.get("exp")
       
       service_prof.description=request.form.get("description")
       service_prof.address=request.form.get("address")
       service_prof.pincode=request.form.get("pincode")
       service_id=db.session.query(Service.id).filter_by(name=service_name)
       service_prof.service_id=service_id
       db.session.commit()

       return redirect("/service")
    
@views.route("/admin/search")
@role_required("admin")
def admin_search():
    search_by = request.args.get('search_by', '')  # The selected option
    search_term = request.args.get('search_term', '')  # The user input for search term
    
    # Base query
    query=Customer.query.join(Service_request).filter(Customer.id==Service_request.customer_id and int(current_user.id)==Service_request.professional_id)


    # Apply the selected filter
    if search_by == 'Service' and search_term:
        query=Service.query.all()
        query1 = query.filter(Service.name.ilike(f'%{search_term}%'))
        query2=query.filter(Service.description.ilike(f"%{search_term}%"))
        query=query1+query2
    elif search_by == 'Service_prof' and search_term:
        query=Service_professional.query.all()
        query1 = query.filter(Service_professional.name.ilike(f'%{search_term}%'))
        query = query.filter(Service_professional.verification_status.ilike(f'%{search_term}%'))
    elif search_by == 'pincode' and search_term:
        query = query.filter(Customer.pincode == search_term)
    results = query.all()
    for service in results:
        for req in service.service_requested:
            print(req)
    return render_template('service_search.html', results=results, search_by=search_by, search_term=search_term)
