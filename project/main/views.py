# project/main/views.py


#################
#### imports ####
#################

from flask import render_template, Blueprint, url_for, redirect, flash, request

from project import app, opalstack
from project.email import send_email
from project.token import generate_confirmation_token, confirm_token
from .forms import RequestForm, PasswordResetForm


################
#### config ####
################

main_blueprint = Blueprint('main', __name__,)


################
#### routes ####
################

@main_blueprint.route('/', methods=['GET', 'POST'])
def home():

    form = RequestForm(request.form)
    if form.validate_on_submit():

        token = generate_confirmation_token(form.mailbox.data)

        reset_url = url_for('main.reset_password', token=token, _external=True)
        html = render_template('main/reset.html',
                               mailbox=form.mailbox.data,
                               reset_url=reset_url)
        subject = "Reset your email password"
        send_email(form.email.data, subject, html)

        flash('A password reset email has been sent.  Check your spam/junk folders if it does not arrive.', 'success')
        return redirect(url_for("main.home"))

    return render_template('main/request_pwdch.html', form=form)


@main_blueprint.route('/reset/<token>', methods=['GET', 'POST'])
def reset_password(token):

    mailbox = confirm_token(token)
    os_mailuser = opalstack.get_mailuser(mailbox) if mailbox else None

    if not mailbox or os_mailuser is None:
        flash('Invalid token. Possibly expired.  Request a new password-reset token.', 'danger')
        return redirect(url_for('main.home'))

    form = PasswordResetForm(request.form)
    if form.validate_on_submit():
        success = opalstack.change_password(os_mailuser, form.password.data)
        if success:
            flash('Password successfully changed.', 'success')
            return redirect(url_for('main.reset_password_success'))
        else:
            flash('Password change was unsuccessful. Probably invaild. Try again.', 'danger')
    else:
        flash('You can now change your password.', 'success')

    return render_template('main/reset_passwod.html', form=form)


@main_blueprint.route('/reset-success/')
def reset_password_success():

    opalstack_webmail_url = app.config['OPALSTACK_WEBMAIL_URL']

    return render_template('main/reset_passwod_success.html', opalstack_webmail_url=opalstack_webmail_url)

