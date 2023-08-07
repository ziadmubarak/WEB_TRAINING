from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from .models import User, PlayerInput
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from .forms import SignUpForm, PlayerInputForm

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                player_input = PlayerInput.query.filter_by(user_id=user.id).first()
                if user.role == 'player' and player_input is None:
                    return redirect(url_for('auth.player_input'))
                else:
                    return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    form = SignUpForm()
    if form.validate_on_submit():
        email = form.email.data
        first_name = form.first_name.data
        password1 = form.password1.data
        password2 = form.password2.data
        role = form.role.data

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='sha256'), role=role)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            if role == 'player':
                return redirect(url_for('auth.player_input'))
            else:
                return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user, form=form)

@auth.route('/player-input', methods=['GET', 'POST'])
@login_required
def player_input():
    form = PlayerInputForm()
    if form.validate_on_submit():
        player_input = PlayerInput(
            user_id=current_user.id,
            position=form.position.data,
            height=form.height.data,
            weight=form.weight.data,
            finishing=form.finishing.data,
            shooting=form.shooting.data,
            handles=form.handles.data,
            rebounding=form.rebounding.data,
            defense=form.defense.data
        )
        db.session.add(player_input)
        db.session.commit()
        flash('Your input has been saved.', category='success')
        return redirect(url_for('views.home'))
    return render_template('player_input.html', user=current_user, form=form)





