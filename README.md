# Gym Membership System 🏋️‍♂️

A Django-based web application for managing gym memberships, member details, and admin dashboard functionalities.

## Features

* **Member Management**: Add, edit, and view members.
* **QR Code Scanning**: For quick member check-ins.
* **Admin Dashboard**: Monitor members and manage data efficiently.
* **Authentication**: Secure login system for admins.

## Live Demo

You can access the live project here: [Gym Membership System](https://gym-membership-system-1.onrender.com/)

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/mohamed-hossam1/gym_membership_system.git
cd gym_membership_system
```

### 2. Create and activate virtual environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run migrations

```bash
python manage.py migrate
```

### 5. Create a superuser

```bash
python manage.py createsuperuser
```

### 6. Run the development server

```bash
python manage.py runserver
```

Then open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

## Technologies Used

* **Backend**: Django (Python)
* **Database**: SQLite (default, can switch to PostgreSQL)
* **Frontend**: HTML, CSS, JavaScript
* **Deployment**: Render

