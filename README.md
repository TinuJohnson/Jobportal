# Job Portal

A full-featured Django-based job portal that connects job seekers with employers. The platform allows employers to post jobs and manage applications, while job seekers can browse jobs and apply for positions.

## Features

### 👥 User Roles
- **Job Seekers**: Browse jobs, apply to positions, manage applications
- **Employers**: Post jobs, manage job listings, review applications
- **Admin** : Manage Users & Jobs (In-build in SQLite)
    (username : anu,
     Password : 2003)

### 💼 Job Management
- Create, read, update, and delete job postings
- Job categories and search functionality
- Company and location-based filtering

### 📄 Application System
- Job seekers can apply to jobs with cover letters and resumes
- Employers can manage and track applications
- Application status tracking (Pending, Reviewed, Shortlisted, Accepted, Rejected)

### 🔐 Authentication & Authorization
- User registration with role selection (Seeker/Employer)
- Secure login/logout system
- Role-based access control

## Technology Stack

- **Backend**: Django 5.2.6
- **Database**: SQLite (default, can be configured for PostgreSQL/MySQL)
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **File Uploads**: Resume handling with validation
- **Authentication**: Django's built-in authentication system

## Installation

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/TinuJohnson/Jobportal
   cd Jobportal

2. **Create a virtual environment**
    python -m venv venv
    venv\Scripts\activate

3. **Run migrations**
    python manage.py makemigrations
    python manage.py migrate

4. **Create a Superuser**
    python manage.py createsuperuser

5. **python manage.py createsuperuser**
    Open your browser and go to http://127.0.0.1:8000

    **PROJECT STRUCTURE**
    
    Jobportal/
    ├── Portal/                 # Django project settings
    ├── templates/             # HTML templates
    │   ├── base.html         # Base template
    │   ├── employer/         # Employer-specific templates
    │   └── seeker/           # Seeker-specific templates              
    ├── media/                # User-uploaded files (resumes)
    ├── manage.py            # Django management script
    ├── db.sqlite3             # Manage Database
    ├── README.md               # Instructions
    └── requirements.txt