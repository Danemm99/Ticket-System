from flask import Flask
from config import settings
from presentation.views import user_routes, ticket_routes, group_routes
from database import db, bcrypt, migrate, login_manager
from presentation.models.group import Group
from presentation.models.user import User
from presentation.models.ticket import Ticket


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = settings.SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = settings.SQLALCHEMY_TRACK_MODIFICATIONS

    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'routes.login'
    login_manager.login_message_category = 'info'

    app.register_blueprint(user_routes.user)
    app.register_blueprint(ticket_routes.ticket)
    app.register_blueprint(group_routes.group)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(reload=True)
