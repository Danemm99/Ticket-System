from database import db


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    users = db.relationship('User', backref='group', lazy=True)
    tickets = db.relationship('Ticket', backref='group', lazy=True)
