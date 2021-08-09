from flask import g, render_template, request, redirect, url_for, flash
from .forms import LoginForm, RegisterForm, EditProfileForm
from app.blueprints.main.forms import SearchForm
from .models import User
from flask_login import login_user, logout_user, current_user, login_required
from .import bp as auth

#Routes
@auth.route('/', methods=['GET'])
def index():
    # form = SearchForm()
    # g.form=form
    return render_template('index.html.j2')

@auth.route('/register', methods=['GET','POST'])
def register():
    form = SearchForm()
    g.form=form
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        try:
            new_user_data={
                "first_name": form.first_name.data.title(),
                "last_name": form.last_name.data.title(),
                "email": form.email.data.lower(),
                "icon": int(form.icon.data),
                "password": form.password.data
            }
            new_user_object = User()
            new_user_object.from_dict(new_user_data)
        except:
            flash('There was a problem creating your account. Please try again','danger')
            return render_template('register.html.j2',form=form)
        # Give the user some feedback that says registered successfully 
        # message, category
        flash('You have registered successfully','success')
        return redirect(url_for('auth.login'))

    return render_template('register.html.j2',form=form)

@auth.route('/login', methods=['GET','POST'])
def login():
    form = SearchForm()
    g.form=form
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        # Do login Stuff
        email = form.email.data.lower()
        password = form.password.data
        u = User.query.filter_by(email=email).first()
        print(u)
        if u is not None and u.check_hashed_password(password):
            login_user(u)
            # Give User feeedback of success
            flash('You have logged in successfully','success')
            return redirect(url_for('social.index'))
        else:
            # Give user Invalid Password Combo error
            flash('Invalid username/password','danger')
            return redirect(url_for('auth.login'))
    return render_template("login.html.j2", form=form)

@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    if current_user is not None:
        logout_user()
        flash('You have logged out','warning')
        return redirect(url_for('social.index'))

@auth.route('/edit_profile', methods=['GET','POST'])
def edit_profile():
    form = SearchForm()
    g.form=form
    form = EditProfileForm()
    if request.method == 'POST' and form.validate_on_submit():
        new_user_data={
            "first_name": form.first_name.data.title(),
            "last_name": form.last_name.data.title(),
            "email": form.email.data.lower(),
            "icon": int(form.icon.data) if int(form.icon.data) !=9000 else current_user.icon,
            "password": form.password.data
        }
        user=User.query.filter_by(email=form.email.data.lower()).first()
        if user and current_user.email != user.email:
            flash('Email in use', 'danger')
            return redirect('auth.edit_profile')
        try:
            current_user.from_dict(new_user_data)
            flash('Your profile has been updated', 'success')
            return redirect(url_for('social.index'))
        except:
            flash('There was a problem creating your account. Please try again','danger')
            return redirect('auth.edit_profile')
    return render_template('register.html.j2',form=form)