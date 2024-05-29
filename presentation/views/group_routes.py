from database import db
from presentation.models.group import Group
from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import current_user, login_required
from permissions import admin_required, not_analyst_required
from presentation.forms.groups import EditGroupForm, CreateGroupForm


group = Blueprint('group_routes', __name__)


@group.route('/home/create_group', methods=['GET', 'POST'])
@login_required
@admin_required
def create_group():
    form = CreateGroupForm()
    if form.validate_on_submit():
        group = Group.query.filter_by(name=form.name.data).first()
        if not group:
            group = Group(name=form.name.data)
            db.session.add(group)
            db.session.commit()
            return redirect(url_for('group_routes.create_group'))
    return render_template('groups/create_group.html', form=form)


@group.route('/home/groups', methods=['GET'])
@login_required
@not_analyst_required
def view_all_groups():
    groups = ''
    if current_user.role == 'admin':
        groups = Group.query.all()
    elif current_user.role == 'manager':
        groups = Group.query.filter_by(id=current_user.group_id)

    return render_template('groups/view_all_groups.html', groups=groups)


@group.route('/home/groups/<int:group_id>', methods=['GET'])
@login_required
@not_analyst_required
def view_group(group_id):
    group = Group.query.get_or_404(group_id)
    return render_template('groups/view_group.html', group=group)


@group.route('/home/groups/<int:group_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_group(group_id):
    group = Group.query.get_or_404(group_id)
    form = EditGroupForm()

    if form.validate_on_submit():
        group.name = form.name.data
        db.session.commit()
        flash('Group name has been updated!', 'success')
        return redirect(url_for('group_routes.view_group', group_id=group.id))

    elif request.method == 'GET':
        form.name.data = group.name

    return render_template('groups/edit_group.html', form=form, group=group)
