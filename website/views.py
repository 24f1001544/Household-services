from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Service
from . import db
import json

views = Blueprint('views', __name__)

@views.route("/")
def home():
    return render_template("home.html")
@views.route("/customer")
def customer():
    services=Service.query.all()
    return render_template("customer.html",services=services)
