import datetime

from flask import Blueprint, render_template, jsonify, request, abort
from flask_login import login_required

from app import db, Constant
from app.models import Activity, Card, Center, Check, Exercise, Machine, Measurement, User

mod_api = Blueprint('api', __name__, url_prefix='/api')


@mod_api.route('/check', methods=['POST'])
def index():
    if not request.json or not 'center_id' in request.json or not 'card_id' in request.json:
        return jsonify({'open': False}), 400
    if not db.session.query(Card).filter_by(card_id=request.json['card_id']).first():
        return jsonify({'open': False})
    last_check = db.session.query(Check).filter_by(card_id=request.json['card_id']) \
        .order_by(Check.time.desc()).first()
    in_out = True
    if last_check:
        if last_check.in_out:
            in_out = False
    check = Check(card_id=request.json['card_id'],
                  center_id=request.json['center_id'],
                  time=datetime.datetime.now(),
                  in_out=in_out)
    db.session.add(check)
    db.session.commit()
    return jsonify({'open': True}), 201


@mod_api.route('/exercise', methods=['POST'])
def exercise():
    if not request.json or not 'time' in request.json or not 'card_id' in request.json:
        return jsonify({'success': False}), 400
    if 'speed' in request.json:
        constants = db \
            .session \
            .query(Constant) \
            .filter_by(activity_id=db
                       .session
                       .query(Machine)
                       .filter_by(machine_id=request.json['machine_id'])
                       .first()
                       .activity_id).all()
        consts = {}
        for i in range(0, len(constants)):
            consts[constants[i].speed] = constants[i]
        constant = consts[min(consts, key=lambda x: abs(x - request.json['speed']))]
    else:
        constant = db.session.query(Constant) \
            .filter_by(activity_id=db
                       .session
                       .query(Machine)
                       .filter_by(machine_id=request.json['machine_id'])
                       .first()
                       .activity_id) \
            .first()
    user = db.session.query(Card).filter_by(card_id=request.json['card_id']).first().user
    if not user:
        return jsonify({'success': False})
    last_measurement = db.session.query(Measurement) \
        .order_by(Measurement.measure_id.desc()) \
        .filter_by(user_id=user.user_id) \
        .first()
    xercise = Exercise(
        time=request.json['time'],
        burnt_calories=(constant.constant * last_measurement.weight * (request.json['time'] / 60)),
        user_id=user.user_id,
        constant_id=constant.constant_id,
        machine_id=request.json['machine_id'],
        datetime=datetime.datetime.now()
    )
    db.session.add(xercise)
    db.session.commit()

    return jsonify({'burnt_calories': float("{0:.2f}".format(xercise.burnt_calories)), 'time': float("{0:.2f}".format(xercise.time))}), 201
