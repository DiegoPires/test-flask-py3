from flask import render_template, redirect, url_for, flash, request
from . import auth
from app import db
from app.email import send_email
from .forms import LoginForm, RegistrationForm
from ..models import User
from flask.ext.login import login_user, logout_user, current_user, login_required

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            # method provided by the flask-login
            login_user(user, form.remember_me.data)
            # next it's the variable used on the querystring when the user
            # tried to access a private area and were redirect to the login page
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    # again, method provided by the flask-login library
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        u = User(email=form.email.data,
                 username=form.username.data,
                 password=form.password.data)

        db.session.add(u)
        db.session.commit()

        # little cat to save our token because i cant send email from here
        token = u.generate_confirmation_token()
        u.token = token
        db.session.add(u)
        db.session.commit()

        send_email(u.email, 'Confirm Your Account',
                   'auth/email/confirm', user=u, token=token)

        flash('You can now login')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('You have confirmed you account')
    else:
        flash('the confirmation link is invalid or expired')
    return redirect(url_for('main.index'))


# before each request from the auth route confirms if the user has confirmed his registry
@auth.before_app_request
def before_request():
    if current_user.is_authenticated() \
            and not current_user.confirmed \
            and request.endpoint[:5] != 'auth.':
        return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous() or current_user.confirmed:
        return redirect('main.index')
    return render_template('auth/unconfirmed.html')


@auth.route('/resend_confirmation')
def resend_confirmation():
    token = current_user.generate_confirmation_token()

    current_user.token = token
    db.session.add(current_user)
    db.session.commit()

    send_email(current_user.email, 'Confirm Your Account',
               'auth/email/confirm', user=current_user, token=token)
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('main.index'))


@auth.route('/secret')
@login_required
def secret():
    return "Only authenticated user"