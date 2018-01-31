import flask
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from app import User, db
from app.forms import RegisterForm, LoginForm

mod_auth = Blueprint('auth', __name__)


@mod_auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        admin = False
        if db.session.query(User).count() == 0:
            admin = True
        user = User(first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    street=form.street.data,
                    house_number=form.house_number.data,
                    zip_code=form.zip_code.data,
                    city=form.city.data,
                    phone_number=form.phone_number.data,
                    email=form.email.data,
                    password=generate_password_hash(form.password.data),
                    admin=admin
                    )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@mod_auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = db.session.query(User).filter_by(email=form.email.data).first()
        if not user:
            form.email.errors.append('Geen gebruiker met dit email adres gevonden')
            return render_template('auth/login.html', form=form)
        if check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('dashboard.index'))
        else:
            form.password.errors.append('Wachtwoord in incorrect')
            return render_template('auth/login.html', form=form)
    return render_template('auth/login.html', form=form)


@mod_auth.route('/signout', methods=['GET', 'POST'])
@login_required
def signout():
    logout_user()
    return redirect(url_for('auth.login'))


@mod_auth.route('/home', methods=['GET', 'POST'])
def home():
    return redirect(url_for('auth.login'))
