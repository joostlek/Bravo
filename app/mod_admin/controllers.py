from functools import wraps

from flask import Blueprint, redirect, url_for, render_template, request
from flask_login import current_user, login_required

from app import db
from app.forms import CenterForm, CardForm, ActivityForm, MachineForm
from app.models import Activity, Card, Center, Check, Exercise, Machine, Measurement, User

mod_admin = Blueprint('admin', __name__, url_prefix='/admin')


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.admin:
            return redirect(url_for('dashboard.index'))
        return f(*args, **kwargs)
    return decorated_function


@mod_admin.route('/')
@login_required
@admin_required
def admin_center():
    amounts = []
    amounts.insert(len(amounts), {'entity': 'Activities', 'amount': db.session.query(Activity).count()})
    amounts.insert(len(amounts), {'entity': 'Cards', 'amount': db.session.query(Card).count()})
    amounts.insert(len(amounts), {'entity': 'Centers', 'amount': db.session.query(Center).count()})
    amounts.insert(len(amounts), {'entity': 'Checks', 'amount': db.session.query(Check).count()})
    amounts.insert(len(amounts), {'entity': 'Exercises', 'amount': db.session.query(Exercise).count()})
    amounts.insert(len(amounts), {'entity': 'Machines', 'amount': db.session.query(Machine).count()})
    amounts.insert(len(amounts), {'entity': 'Measurements', 'amount': db.session.query(Measurement).count()})
    amounts.insert(len(amounts), {'entity': 'Users', 'amount': db.session.query(User).count()})
    return render_template('admin/admin_center.html', amounts=amounts)


@mod_admin.route('/centers')
@login_required
@admin_required
def centers():
    return render_template('admin/centers.html', db=db, Center=Center)


@mod_admin.route('/centers/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_center():
    form = CenterForm(request.form)
    if request.method == 'POST' and form.validate():
        center = Center(name=form.name.data,
                        street=form.street.data,
                        house_number=form.house_number.data,
                        zip_code=form.zip_code.data,
                        city=form.city.data)
        db.session.add(center)
        db.session.commit()
        return redirect(url_for('admin.centers'))
    return render_template('admin/add/center.html', form=form, callback=url_for('admin.add_center'))


@mod_admin.route('/centers/edit/<int:center_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_center(center_id):
    center = db.session.query(Center).filter_by(center_id=center_id).first()
    form = CenterForm(request.form, center)
    if request.method == 'POST' and form.validate():
        form.populate_obj(center)
        db.session.commit()
        return redirect(url_for('admin.centers'))
    return render_template('admin/add/center.html', form=form, callback=url_for('admin.edit_center',
                                                                                center_id=center_id))


@mod_admin.route('/centers/delete/<int:center_id>')
@login_required
@admin_required
def delete_center(center_id):
    center = db.session.query(Center).filter_by(center_id=center_id).first()
    db.session.delete(center)
    db.session.commit()
    return redirect(url_for('admin.centers'))


@mod_admin.route('/checks')
@login_required
@admin_required
def checks():
    return render_template('admin/checks.html', db=db, Check=Check)


@mod_admin.route('/cards')
@login_required
@admin_required
def cards():
    return render_template('admin/card.html', db=db, Card=Card)


@mod_admin.route('/cards/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_card():
    form = CardForm(request.form)
    form.user_id.choices = [(user.user_id, user.construct_name()) for user in db.session.query(User).all()]
    if request.method == 'POST' and form.validate():
        card = Card(user_id=form.user_id.data,
                    active=True)
        user = db.session.query(User).filter_by(user_id=form.user_id.data).first()
        user.cards.append(card)
        db.session.add(card)
        db.session.commit()
        return redirect(url_for('admin.cards'))
    return render_template('admin/add/card.html', form=form)


@mod_admin.route('/activities')
@login_required
@admin_required
def activities():
    return render_template('admin/activities.html', db=db, Activity=Activity)


@mod_admin.route('/activities/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_activity():
    form = ActivityForm(request.form)
    if request.method == 'POST' and form.validate():
        activity = Activity(name=form.name.data)
        db.session.add(activity)
        db.session.commit()
        return redirect(url_for('admin.activities'))
    return render_template('admin/add/activity.html', form=form)


@mod_admin.route('/machines')
@login_required
@admin_required
def machines():
    return render_template('admin/machines.html', db=db, Machine=Machine)


@mod_admin.route('/machines/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_machine():
    form = MachineForm(request.form)
    form.activity_id.choices = [(activity.activity_id, activity.name) for activity in db.session.query(Activity).all()]
    form.center_id.choices = [(center.center_id, center.name) for center in db.session.query(Center).all()]
    if request.method == 'POST' and form.validate():
        machine = Machine(
            activity_id=form.activity_id.data,
            center_id=form.center_id.data
        )
        center = db.session.query(Center).filter_by(center_id=form.center_id.data).first()
        activity = db.session.query(Activity).filter_by(activity_id=form.activity_id.data).first()
        center.machines.append(machine)
        activity.machines.append(machine)
        db.session.add(machine)
        db.session.commit()
        return redirect(url_for('admin.machines'))
    return render_template('admin/add/machine.html', form=form)


@mod_admin.route('/users')
@login_required
@admin_required
def users():
    return render_template('admin/users.html', db=db, User=User)

