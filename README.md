# Enterprise Management System (EMS)

A web-based Enterprise Management System built with Django to manage employees, projects, tasks, and user permissions.

## Overview

Enterprise Management System is a Django application designed to simplify internal company management.

The application allows administrators, managers, and employees to collaborate through a role-based access system.

## Features

### Authentication & Authorization

* Custom user model with email authentication
* Role-based access control:

  * Admin
  * Manager
  * Employee
* Protected views using Django permissions

### Employee Management

* Employee profiles
* Employee information management
* Employee status tracking

### Project Management

* Create and manage projects
* Assign managers to projects
* Assign employees to projects
* Track project status

### Task Management

* Create and manage tasks
* Assign tasks to employees
* Task status workflow:

  * Todo
  * In Progress
  * Completed
  * Cancelled
* Task priority levels:

  * Low
  * Medium
  * High

### User Interface

* Responsive design using Bootstrap 5
* Dashboard with company statistics
* Clean tables and cards layout

## Technologies

### Backend

* Python
* Django
* Django ORM

### Frontend

* HTML5
* CSS3
* Bootstrap 5
* JavaScript (Vanilla DOM)

### Database

* MariaDB / MySQL

### Tools

* Git & GitHub
* Visual Studio Code

## Project Structure

```
enterprise-management-system/

├── apps/
│
├── accounts/
│   ├── authentication
│   ├── permissions
│   └── users
│
├── employees/
│   └── employee management
│
├── projects/
│   └── project management
│
├── tasks/
│   └── task management
│
├── templates/
│
├── static/
│
├── manage.py
│
└── requirements.txt
```

## Installation

Clone the repository:

```bash
git clone https://github.com/benmammarfaycal/enterprise-management-system.git
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the environment:

Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create your environment variables:

```bash
.env
```

Apply migrations:

```bash
python manage.py migrate
```

Create an administrator account:

```bash
python manage.py createsuperuser
```

Run the development server:

```bash
python manage.py runserver
```

The application will be available at:

```
http://127.0.0.1:8000/
```

## User Roles

### Admin

Full access:

* Manage users
* Create projects
* Modify projects
* Assign employees
* Manage tasks

### Manager

Can:

* View managed projects
* Create tasks
* Manage project tasks

### Employee

Can:

* View assigned projects
* View assigned tasks
* Update task progress

## Database Model

Main entities:

```
User

Employee

Project

ProjectAssignment

Task
```

Relationships:

```
Employee 1 ---- N Project
(Employee as manager)

Employee N ---- N Project
(through ProjectAssignment)

Project 1 ---- N Task

Employee 1 ---- N Task
```

## Future Improvements

Possible future features:

* Notifications
* Comments
* File attachments
* Time tracking
* Activity history
* Advanced dashboard charts

## Author

Faycal Benmammar

## License

This project is developed for educational and portfolio purposes.
