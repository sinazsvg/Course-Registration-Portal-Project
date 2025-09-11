# Course-Registration-Portal-Project

Course Registration Portal 🎓

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/Flask-2.3.3-green)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3.0-purple)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

A comprehensive Flask-based web application for managing course registrations with role-based access control, beautiful Persian RTL interface, and advanced administrative features.

![Course Registration Portal](https://via.placeholder.com/300x400/AA6572/EEEEEE?text=Courses+Registration)

✨ Features
👨‍🎓 Student Features
User Registration & Authentication - Secure signup/login system

Course Catalog - Browse all available courses with detailed information

Smart Enrollment System - Register for courses with automatic schedule conflict detection

Personal Dashboard - View enrolled courses and academic schedule

Student Profile - Complete profile management system

Schedule Management - Visual timetable of registered courses

🛡 Administrator Features

Advanced Authentication - Two-factor admin verification with admin IDs

Complete Course Management - Create, edit, and delete courses

System Administration - Comprehensive management interface

Real-time Analytics - View enrollment statistics and system status

User Management - Monitor student registrations and activities

🚀 System Features

RTL Support - Complete Persian language interface with right-to-left layout

Responsive Design - Mobile-friendly Bootstrap interface

JSON Database - Lightweight file-based data storage

Session Management - Secure user authentication with role-based access

Comprehensive Logging - Detailed activity logging with daily log files

Schedule Conflict Detection - Prevents overlapping course registrations

🛠 Technology Stack

Backend Framework: Flask 2.3.3

Frontend: HTML5, CSS3, JavaScript, Bootstrap 5.3.0

Database: JSON-based file storage system

Authentication: Session-based with role management

Templating Engine: Jinja2

Logging: Python logging module with daily file rotation

Language Support: Full RTL (Right-to-Left) for Persian language

📦 Installation & Setup

Prerequisites
Python 3.8 or higher

pip (Python package manager)

Step-by-Step Installation
Clone the repository

bash
git clone [https://github.com/sinazsvg/course-registration-portal.git](https://github.com/sinazsvg/Course-Registration-Portal-Project)
cd course-registration-portal
Create and activate virtual environment

bash
# On Windows
python -m venv venv
venv\Scripts\activate
 
# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
Install dependencies

bash
pip install flask
Initialize the application

bash
python app.py
Access the application
Open your web browser and navigate to http://localhost:5000

🏗 Project Structure

text
course-registration-portal/

├── data/                 # JSON data storage

│   ├── users.json        # User accounts and credentials

│   ├── courses.json      # Course information and details

│   ├── registrations.json # Course enrollment records

│   └── admin_ids.json    # Administrator identification codes

├── models/               # Data models and business logic

│   ├── user.py          # User model and authentication logic

│   ├── course.py        # Course model and management logic

│   ├── registration.py  # Registration model and enrollment logic

│   └── schedule.py      # Schedule management and conflict detection

├── templates/           # HTML templates with Jinja2

│   ├── index.html       # Homepage with course catalog

│   ├── login.html       # User authentication page

│   ├── register.html    # User registration page

│   ├── dashboard.html   # User dashboard after login

│   ├── profile.html     # User profile management

│   ├── admin_courses.html # Course management interface
│   ├── create_course.html # Course creation form
│   ├── edit_course.html  # Course editing interface

│   └── verify_admin.html # Admin verification page

├── utils/               # Utility modules and helpers

│   ├── json_handler.py  # JSON file read/write operations

│   ├── authenticator.py # User authentication logic

│   └── logger.py       # Application logging system

├── logs/                # Application logs (auto-generated)

├── app.py              # Main application entry point

└── README.md           # Project documentation

👥 User Roles & Permissions

Student 👨‍🎓

Register new account with student role

Browse available courses in the catalog

Enroll in courses without schedule conflicts

View personal dashboard with enrolled courses

Access and manage personal profile

View academic schedule and timetable

Administrator 🛡

Register with administrator role (requires admin ID)

Access comprehensive admin dashboard

Create new courses with complete details

Edit existing course information

Delete courses and manage content

Monitor all user registrations and activities

View system analytics and statistics

🎯 Usage Guide

For Students
Registration: Create a new account with student role

Authentication: Log in to your account

Course Browsing: Explore available courses from the homepage

Enrollment: Register for courses without schedule conflicts

Dashboard: View your enrolled courses and academic schedule

For Administrators
Registration: Create account with administrator role (requires admin ID)

Authentication: Log in with admin credentials

Dashboard: Access admin dashboard from profile menu

Course Management: Create new courses with complete details

System Maintenance: Manage existing courses and user registrations

🔌 API Endpoints


Method  Endpoint  Description  Access Level

GET  /  Homepage with course catalog  Public

GET/POST  /register  User registration  Public

GET/POST  /login  User authentication  Public

GET  /logout  User logout  Authenticated

GET  /dashboard  User dashboard  Authenticated

GET  /profile  User profile  Authenticated

POST  /enroll  Course enrollment  Students Only

GET  /admin/courses  Course management  Administrators

GET/POST  /admin/create_course  Create course  Administrators

GET/POST  /admin/edit_course/<id>  Edit course  Administrators

POST  /admin/delete_course/<id>  Delete course  Administrators

🎨 UI/UX Features

Modern Responsive Design: Clean Bootstrap-based interface

RTL Support: Complete Persian language support with right-to-left layout

Mobile-First Approach: Works seamlessly on desktop, tablet, and mobile devices

Interactive Elements: Dynamic forms with real-time validation

Professional Styling: Gradient headers and card-based design

User-Friendly Navigation: Intuitive menu structure and workflow

🔒 Security Features

Role-based authentication system

Session management with secure cookies

Admin verification with unique admin IDs

Input validation and data sanitization

Secure password handling

Comprehensive activity logging

Access control for sensitive operations

📝 Logging System

The application includes a comprehensive logging system:

User authentication events (success/failure)

Course management activities (create, update, delete)

Registration changes (enrollment/drop)

System errors and warnings

Daily log files with automatic rotation

Timestamped records for all activities

👨‍💻 Development Team

Sina Zamani - Developer - GitHub

Samin Hashemi - Developer - GitHub

🔮 Future Enhancements

Database migration to SQLite/PostgreSQL

Email notifications system

Advanced reporting and analytics

REST API development

Mobile application interface

Payment integration for course fees

Calendar integration (Google Calendar, etc.)

File upload system for course materials

Grade management system

Attendance tracking functionality

📊 Sample Data

The system includes sample data for demonstration and testing:

Pre-defined admin IDs: ADM-001, ADM-002, ADM-003

Sample courses with various schedules and capacities

Demonstration user accounts for both student and admin roles

🤝 Contributing

We welcome contributions from the community! Please feel free to submit pull requests or open issues for bugs and feature requests.

Fork the project repository

Create your feature branch (git checkout -b feature/AmazingFeature)

Commit your changes (git commit -m 'Add some AmazingFeature')

Push to the branch (git push origin feature/AmazingFeature)

Open a Pull Request

📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

🆘 Support

For support, please contact us at:

Email: sinazamani7362@gmail.com

Issue Tracker: GitHub Issues

Note: This is a university project developed for educational purposes. The system demonstrates full-stack web development capabilities with Flask, including user authentication, database management, and responsive UI design.

⭐️ Star this repository if you find it helpful!
