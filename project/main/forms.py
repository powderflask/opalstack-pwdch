# project/main/forms.py


from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from project import opalstack


class RequestForm(FlaskForm):
    """ Request a reset password link for a specific mailbox"""
    mailbox = StringField(
        'mailbox',
        validators=[DataRequired(), Length(min=6, max=255)])

    email = StringField(
        'email',
        validators=[DataRequired(), Email(message=None), Length(min=6, max=255)])

    def validate(self):
        initial_validation = super(RequestForm, self).validate()
        if not initial_validation:
            return False

        os_mailbox = opalstack.get_mailuser(self.mailbox.data)
        if not os_mailbox:
            self.mailbox.errors.append("This username does not exist on our service")
            return False
        os_email = opalstack.get_email_adderess(self.email.data)
        if not os_email:
            self.email.errors.append("This email does not  exist on our service")
            return False
        return opalstack.validate_email_destination(os_mailbox, os_email)


class PasswordResetForm(FlaskForm):

    # TODO: add validator for Opalstack p/w restrictions  (configurable)

    password = PasswordField(
        'password',
        validators=[DataRequired(), Length(min=6, max=255)]
    )
    confirm = PasswordField(
        'Repeat password',
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match.')
        ]
    )
