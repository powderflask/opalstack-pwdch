# project/token.py

from itsdangerous import URLSafeTimedSerializer

from project import app


def generate_confirmation_token(mailbox):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(mailbox, salt=app.config['SECURITY_PASSWORD_SALT'])


def confirm_token(token, expiration=app.config['TOKEN_EXPIRY_SECONDS']):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        mailbox = serializer.loads(
            token,
            salt=app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration
        )
    except:
        return False
    return mailbox
