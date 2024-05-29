# Ticket-System

The web application, built with Flask, offers a simple ticket system featuring role-based access control (RBAC) and user groups. Users can create, manage, and track tickets with various statuses, assignments, and notes. Admins oversee all groups, while managers and analysts are limited to managing or working with tickets from their assigned group. Groups like Customer 1, Customer 2, and Customer 3 organize users, facilitating efficient ticket management and ensuring access to relevant tickets.

## Installation

**1. Clone the repository to your folder:**
```commandline
git clone https://github.com/Danemm99/Ticket_System.git .
```

**2. Install dependencies:**

```commandline
pip install -r requirements
```

## Create file .env

Create file .env and write there your POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB, POSTGRES_HOST, POSTGRES_PORT and SECRET_KEY.

## Run project

```commandline
flask db upgrade
```

```commandline
set FLASK_APP=app.py
```

```commandline
python app.py
```
