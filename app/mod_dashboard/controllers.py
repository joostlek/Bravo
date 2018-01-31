import datetime
from functools import wraps

import math
from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user

from app import db
from app.forms import MeasurementForm
from app.models import Activity, Card, Center, Check, Exercise, Machine, Measurement, User

mod_dashboard = Blueprint('dashboard', __name__)


@mod_dashboard.route('/')
@login_required
def index():
    amounts = []
    amounts.insert(len(amounts), {'entity': 'Activities', 'amount': db.session.query(Activity).count()})
    amounts.insert(len(amounts), {'entity': 'Cards', 'amount': db.session.query(Card).count()})
    amounts.insert(len(amounts), {'entity': 'Centers', 'amount': db.session.query(Center).count()})
    amounts.insert(len(amounts), {'entity': 'Checks', 'amount': db.session.query(Check).count()})
    amounts.insert(len(amounts), {'entity': 'Exercises', 'amount': db.session.query(Exercise).count()})
    amounts.insert(len(amounts), {'entity': 'Machines', 'amount': db.session.query(Machine).count()})
    amounts.insert(len(amounts), {'entity': 'Measurements', 'amount': db.session.query(Measurement).count()})
    amounts.insert(len(amounts), {'entity': 'Users', 'amount': db.session.query(User).count()})
    return render_template('dashboard/index.html', amounts=amounts)


@mod_dashboard.route('/gewicht')
@login_required
def measurements():
    return render_template('dashboard/measurements.html', db=db, Measurement=Measurement)


@mod_dashboard.route('/gewicht/add', methods=['GET', 'POST'])
@login_required
def add_measurement():
    form = MeasurementForm(request.form)
    if request.method == 'POST' and form.validate():
        measurement = Measurement(
            weight=form.weight.data,
            height=form.height.data,
            date=datetime.date.today()
        )
        current_user.measurements.append(measurement)
        db.session.add(measurement)
        db.session.commit()
        return redirect(url_for('dashboard.measurements'))
    elif request.method == 'GET':
        last_measurement = db.session.query(Measurement)\
            .order_by(Measurement.measure_id.desc())\
            .filter_by(user_id=current_user.user_id)\
            .first()
        if last_measurement:
            form = MeasurementForm(weight=last_measurement.weight, height=last_measurement.height)
        return render_template('dashboard/add/measurement.html', form=form)
    return render_template('dashboard/add/measurement.html', form=form)


@mod_dashboard.route('/statistiek')
@login_required
def stats():
    stat = {}
    count = {}
    for exercise in current_user.exercises:
        date = exercise.datetime.strftime('%m/%Y')
        if date in stat:
            stat[date]['time_active'] += float("{0:.2f}".format(exercise.time))
            stat[date]['burnt_calories'] += float("{0:.2f}".format(exercise.burnt_calories))
        else:
            stat[date] = {}
            stat[date]['time_active'] = float("{0:.2f}".format(exercise.time))
            stat[date]['burnt_calories'] = float("{0:.2f}".format(exercise.burnt_calories))
            stat[date]['visits'] = 0
        if exercise.machine.activity.name in count:
            count[exercise.machine.activity.name] += 1
        else:
            count[exercise.machine.activity.name] = 1
    for card in current_user.cards:
        for check in card.checks:
            if check.in_out:
                date = check.time.strftime('%m/%Y')
                if date in stat:
                    stat[date]['visits'] += 1
                else:
                    stat[date] = {}
                    stat[date]['visits'] = 1
    return render_template('dashboard/statistics.html', db=db, Exercise=Exercise, stats=stat, count=count)


@mod_dashboard.route('/activiteit')
@login_required
def activities():
    return render_template('dashboard/exercises.html', db=db, Exercise=Exercise, math=math)


