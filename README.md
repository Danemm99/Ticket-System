# Ticket-System


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
