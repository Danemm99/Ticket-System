from database import db
from presentation.models.user import User
from presentation.models.group import Group
from presentation.models.ticket import Ticket
from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import current_user, login_required
from permissions import analyst_required, not_analyst_required
from presentation.forms.tickets import EditTicketStatusForm, EditTicketForm, TicketForm
from flask import abort


ticket = Blueprint('ticket_routes', __name__)


@ticket.route('/home/create_ticket', methods=['GET', 'POST'])
@login_required
@not_analyst_required
def create_ticket():
    form = TicketForm()

    if current_user.role == 'admin':
        form.group.choices = [(group.id, group.name) for group in Group.query.all()]
    else:
        form.group.choices = [(current_user.group.id, current_user.group.name)]

    if form.validate_on_submit():
        note = form.note.data
        status = form.status.data
        group_id = form.group.data

        new_ticket = Ticket(note=note, status=status, group_id=group_id)
        db.session.add(new_ticket)
        db.session.commit()

        flash('Ticket created successfully!', 'success')
        return redirect(url_for('user_routes.home'))

    return render_template('tickets/create_ticket.html', form=form)


@ticket.route('/home/groups/<int:group_id>/tickets>', methods=['GET'])
@login_required
@not_analyst_required
def view_tickets(group_id):
    if current_user.role != 'admin' and group_id != current_user.group_id:
        abort(403)

    tickets = db.session.query(Ticket, User.username).outerjoin(User, Ticket.user_id == User.id).filter(
        Ticket.group_id == group_id).all()

    return render_template('tickets/view_tickets.html', tickets=tickets, group_id=group_id)


@ticket.route('/home/my_tickets', methods=['GET'])
@login_required
@analyst_required
def view_my_tickets():
    tickets = Ticket.query.filter_by(user_id=current_user.id)
    return render_template('tickets/view_my_tickets.html', tickets=tickets, group_id=current_user.group_id)


@ticket.route('/home/groups/<int:group_id>/tickets/<int:ticket_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_ticket(group_id, ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)

    if current_user.role != 'admin':
        if ticket.user_id != current_user.id:
            abort(403)

    if current_user.role == 'analyst':
        form = EditTicketStatusForm()
    else:
        form = EditTicketForm()

    if form.validate_on_submit():
        ticket.status = form.status.data
        if current_user.role != 'analyst':
            ticket.note = form.note.data
        db.session.commit()
        if current_user.role != 'analyst':
            return redirect(url_for('group_routes.view_group', group_id=group_id))
        else:
            tickets = Ticket.query.filter_by(user_id=current_user.id)
            return render_template('tickets/view_my_tickets.html', tickets=tickets, group_id=group_id)

    elif request.method == 'GET':
        form.status.data = ticket.status
        if current_user.role != 'analyst':
            form.note.data = ticket.note

    return render_template('tickets/edit_ticket.html', form=form, ticket=ticket)
