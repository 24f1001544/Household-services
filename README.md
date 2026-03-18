# Household Services Platform

This is an IITM MAD-1 project. A comprehensive web application for connecting customers with household service professionals.

## Project Overview

The Household Services Platform is a full-stack web application built with Flask (backend) and Vue.js (frontend) that facilitates the connection between customers needing household services and verified service professionals. The platform includes role-based access for customers, service professionals, and administrators, with features for service requests, professional verification, reviews, and service management.

## Features

### User Management
- **Multi-role Authentication**: Separate login/signup for customers, service professionals, and administrators
- **Profile Management**: Users can view and edit their profiles
- **Secure Password Hashing**: Using Werkzeug security for password management

### Customer Features
- Browse available services
- Search for service professionals by name, location, or pincode
- Request services from professionals
- View service request history and status
- Submit reviews and ratings for completed services
- Dashboard with service request statistics

### Service Professional Features
- Register with service details and upload verification documents
- View and manage service requests (accept/reject)
- Search for customers and service requests
- Profile management with experience and description
- View assigned service requests

### Administrator Features
- Manage services (add, edit, delete)
- Verify or reject service professional applications
- View all service professionals and their verification status
- Access to system-wide statistics and management tools
- Search functionality for services and professionals

### Core Functionality
- **Service Requests**: Customers can request services, professionals can accept/reject
- **Review System**: Rating and feedback for completed services
- **Search and Filter**: Advanced search capabilities for all user types
- **Document Upload**: Service professionals can upload verification documents (PDF)
- **Status Tracking**: Real-time status updates for service requests

## Installation Steps

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Git

### Backend Setup
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd Household-services
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirement.txt
   ```

4. Run the Flask application:
   ```bash
   python main.py
   ```

5. Access the application at `http://localhost:5001`

### Frontend Setup (if applicable)
Note: The frontend Vue.js application setup is not included in the current workspace. If the frontend directory is available:

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install Node.js dependencies:
   ```bash
   npm install
   ```

3. Run the development server:
   ```bash
   npm run serve
   ```

## API Documentation

The application uses Flask routes for web endpoints. Below are the main API endpoints:

### Authentication Endpoints
- `POST /login` - User login
- `POST /signup` - User registration

### Customer Endpoints
- `GET /customer` - Customer dashboard
- `POST /customer/request/<service_id>` - Request a service
- `POST /customer/service_request/<request_id>` - Close service and submit review
- `GET /customer/search` - Search for service professionals
- `GET /customer/profile` - View customer profile
- `POST /customer/profile/edit` - Edit customer profile

### Service Professional Endpoints
- `GET /service` - Service professional dashboard
- `POST /service/<service_id>` - Accept/reject service request
- `GET /service/search` - Search for customers
- `GET /service/profile` - View service professional profile
- `POST /service/profile/edit` - Edit service professional profile

### Administrator Endpoints
- `GET /admin` - Admin dashboard
- `POST /admin/<id>` - Verify/reject service professional
- `GET /edit/<service_id>` - Edit service (GET)
- `POST /edit/<service_id>` - Edit service (POST)
- `POST /delete/<service_id>` - Delete service
- `GET /newService` - Add new service (GET)
- `POST /newService` - Add new service (POST)
- `GET /admin/search` - Admin search
- `GET /admin/viewprof/<prof_id>` - View professional profile
- `GET /admin/viewprof/serve_pdf/<prof_id>` - Download professional document

### General Endpoints
- `GET /dashboard` - User dashboard with statistics
- `GET /` - Home page (requires login)

### Response Formats
- Web pages are rendered using Jinja2 templates
- JSON responses for AJAX requests where applicable
- File downloads for document serving

### Authentication
All endpoints except `/login` and `/signup` require user authentication. Role-based access control is implemented using Flask-Login and session management.

### Database
The application uses SQLite with SQLAlchemy ORM. Tables include:
- Admin
- Customer
- Service
- Service_professional
- Service_request
- Reviews
- Prof_req
