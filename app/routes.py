import sqlalchemy as sa

from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from urllib.parse import urlsplit

from app import app, forms, db, prediction_model
from app.models import User


@app.route('/')
@app.route('/home')
def home():
    if current_user.is_authenticated:
        return render_template('home.html', title='Home', username=current_user.username)
    else:
        return render_template('home.html', title='Home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = forms.LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = forms.RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/get_recommendations', methods=['GET', 'POST'])
@login_required
def get_recommendations():
    form = forms.PredictionForm()
    form.recommendation.choices = prediction_model.get_prediction(current_user.liked_tracks_ids)
    if form.validate_on_submit():
        current_user.update_liked_tracks(form.recommendation.data)
        db.session.commit()
        return redirect(url_for('get_recommendations'))
    return render_template('get_recommendations.html', title='Recommendations', form=form)


@app.route('/clear_user_info', methods=['GET', 'POST'])
@login_required
def clear_user_info():
    form = forms.ClearUserInfoForm()
    if form.validate_on_submit():
        current_user.clear_liked_tracks()
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('clear_user_info.html', title='Clear User Info', form=form)


@app.route('/get_liked_tracks')
@login_required
def get_liked_tracks():
    tracks = prediction_model.get_tracks_by_ids(current_user.liked_tracks_ids)
    return render_template('get_liked_tracks.html', title='Liked Tracks', tracks=tracks)
