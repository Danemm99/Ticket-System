from database import db, bcrypt
from presentation.models.user import User
from presentation.models.group import Group
from presentation.models.ticket import Ticket
from flask import Blueprint, render_template, url_for, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from permissions import admin_required, not_analyst_required
from presentation.forms.users import SignUpForm, LoginForm, AddManagerForm, ManageAnalystForm
from flask import abort


user = Blueprint('user_routes', __name__)


@user.route('/')
def main():
    if current_user.is_authenticated:
        return redirect(url_for('user_routes.home'))
    return render_template('users/main.html')


@user.route('/home')
@login_required
def home():
    return render_template('users/home.html', user=current_user)


@user.route("/signup", methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('user_routes.home'))

    form = SignUpForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        role = form.role.data

        existing_user = User.query.filter_by(username=username).first()
        existing_email = User.query.filter_by(email=email).first()

        if not existing_user and not existing_email:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            new_user = User(username=username, email=email, role=role, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('user_routes.login'))
    return render_template('users/signup.html', form=form)


@user.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('user_routes.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=True)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('user_routes.home'))
    return render_template('users/login.html', title='Login', form=form)


@user.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('user_routes.main'))


@user.route('/home/add_manager', methods=['GET', 'POST'])
@login_required
@admin_required
def add_manager():
    form = AddManagerForm()
    form.group_id.choices = [(g.id, g.name) for g in Group.query.all()]
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            user.group_id = form.group_id.data
            db.session.commit()
            return redirect(url_for('user_routes.add_manager'))
    return render_template('users/add_manager.html', form=form)


@user.route('/home/groups/<int:group_id>/remove_manager/<int:manager_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def remove_manager(group_id, manager_id):
    group = Group.query.get_or_404(group_id)
    manager = User.query.get_or_404(manager_id)

    if request.method == 'POST':
        if 'delete' in request.form:
            group.users.remove(manager)
            db.session.commit()
            return redirect(url_for('group_routes.view_group', group_id=group_id))
        elif 'return' in request.form:
            return redirect(url_for('group_routes.view_group', group_id=group_id))

    return render_template('users/remove_manager.html', group=group, manager=manager)


@user.route('/home/groups/<int:group_id>/managers', methods=['GET'])
@login_required
@not_analyst_required
def view_managers(group_id):
    if current_user.role != 'admin' and group_id != current_user.group_id:
        abort(403)

    group = Group.query.get_or_404(group_id)
    managers = User.query.filter_by(group_id=group_id, role='manager').all()
    return render_template('users/view_managers.html', group=group, managers=managers)


@user.route('/home/groups/<int:group_id>/analysts', methods=['GET'])
@login_required
@not_analyst_required
def view_analysts(group_id):
    if current_user.role != 'admin' and group_id != current_user.group_id:
        abort(403)

    group = Group.query.get_or_404(group_id)
    analysts = User.query.filter_by(group_id=group_id, role='analyst').all()
    return render_template('users/view_analysts.html', group=group, analysts=analysts)


@user.route('/home/groups/<int:group_id>/tickets/<int:ticket_id>/manage_analyst', methods=['GET', 'POST'])
@login_required
@not_analyst_required
def manage_analyst(group_id, ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)

    if current_user.role != 'admin':
        if ticket.group_id != current_user.group_id:
            abort(403)

    form = ManageAnalystForm()

    available_analysts = User.query.filter(
        (User.role == 'analyst') &
        ((User.group_id == None) | (User.group_id == ticket.group_id)) &
        (User.id != ticket.user_id)
    ).all()
    form.analyst.choices = [(user.id, user.username) for user in available_analysts]

    if form.validate_on_submit():
        new_analyst_id = form.analyst.data
        new_analyst = User.query.get_or_404(new_analyst_id)

        if ticket.user_id:
            current_analyst = User.query.get(ticket.user_id)

            other_tickets = Ticket.query.filter(Ticket.user_id == current_analyst.id, Ticket.id != ticket.id).all()
            if not other_tickets:
                current_analyst.group_id = None

        ticket.user_id = new_analyst_id
        new_analyst.group_id = ticket.group_id
        db.session.commit()

        return redirect(url_for('group_routes.view_group', group_id=ticket.group_id))

    return render_template('users/manage_analyst.html', form=form, ticket=ticket)


@user.route('/home/groups/<int:group_id>/remove_analyst/<int:analyst_id>', methods=['GET', 'POST'])
@login_required
@not_analyst_required
def remove_analyst(group_id, analyst_id):
    group = Group.query.get_or_404(group_id)
    analyst = User.query.get_or_404(analyst_id)

    if current_user.role != 'admin':
        if analyst.group_id != current_user.group_id:
            abort(403)

    if request.method == 'POST':
        if 'delete' in request.form:
            tickets = Ticket.query.filter_by(user_id=analyst.id).all()
            for ticket in tickets:
                ticket.user_id = None
            analyst.group_id = None
            db.session.commit()
            return redirect(url_for('group_routes.view_group', group_id=group.id))
        elif 'return' in request.form:
            return redirect(url_for('group_routes.view_group', group_id=group.id))

    return render_template('users/remove_analyst.html', group=group, analyst=analyst)
