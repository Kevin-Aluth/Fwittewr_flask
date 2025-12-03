from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, login_user, logout_user, current_user
from ..forms import LoginForm, RegisterForm
from ..models import User
from ..extensions import db, bcrypt


auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                flash('login successful', category='success')
                return redirect(url_for('home.posts'))
        flash('Error: username and/or password incorrect', category='error')

    return render_template('authentication/login.html', form=form)

@auth_bp.route('/logout', methods=['GET'])
def logout():
    if current_user.is_authenticated:
        logout_user()
    
    return redirect(url_for('auth.login'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register(): 
    form = RegisterForm()

    if form.validate_on_submit():
        password = bcrypt.generate_password_hash(form.password.data)
        user = User(username=form.username.data, password=password)
        db.session.add(user)
        db.session.commit()
        flash('successfully registered', category='success')
        return redirect(url_for('auth.login'))
    elif request.method == 'POST':
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'Error in field {field}: {error}', category='error')

    return render_template('authentication/register.html', form=form)
