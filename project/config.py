# project/config.py

import os
import configparser

basedir = os.path.abspath(os.path.dirname(__file__))


def _get_bool_env_var(varname, default=None):

    value = os.environ.get(varname, default)

    if value is None:
        return False
    elif isinstance(value, str) and value.lower() == 'false':
        return False
    elif bool(value) is False:
        return False
    else:
        return bool(value)


class BaseConfig(object):
    """Base configuration."""
    config_path = None  # Overrride to load config file

    # main config
    SECRET_KEY = 'The Answer is 42'
    SECURITY_PASSWORD_SALT = 'The question is questionable?'
    DEBUG = False
    BCRYPT_LOG_ROUNDS = 13
    WTF_CSRF_ENABLED = True
    DEBUG_TB_ENABLED = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False

    TOKEN_EXPIRY_SECONDS = 60 * 60 * 24   # Tokens expire after 1 day

    # mail settings
    # defaults are:
    #  - MAIL_SERVER = 'smtp.de.opalstack.com'
    #  - MAIL_PORT = 587
    #  - MAIL_USE_TLS = True
    #  - MAIL_USE_SSL = True
    MAIL_SERVER = os.environ.get('APP_MAIL_SERVER', 'smtp.de.opalstack.com')
    MAIL_PORT = int(os.environ.get('APP_MAIL_PORT', 587))
    MAIL_USE_TLS = _get_bool_env_var('APP_MAIL_USE_TLS', True)
    MAIL_USE_SSL = _get_bool_env_var('APP_MAIL_USE_SSL', False)

    # mail authentication
    MAIL_USERNAME = os.environ.get('APP_MAIL_USERNAME', None)
    MAIL_PASSWORD = os.environ.get('APP_MAIL_PASSWORD', None)

    # mail accounts
    MAIL_DEFAULT_SENDER = 'from@example.com'

    # Opalstack settings
    OPALSTACK_API_URL = 'https://my.opalstack.com/'
    OPALSTACK_API_VERSION = 'v0'
    OPALSTACK_WEBMAIL_URL = 'https://webmail.opalstacked.com'
    OPALSTACK_API_TOKEN = 'get an API token from opalstack control panel'

    @classmethod
    def load_config_file(cls, config_path):
        # if config file exists, read it - takes precendence over defaults specfied by the config class
        if os.path.isfile(config_path):
            config = configparser.ConfigParser()

            config.read(config_path)

            cls.SECRET_KEY = config.get('keys', 'SECRET_KEY')
            cls.SECURITY_PASSWORD_SALT = config.get('keys', 'SECRET_KEY')

            # mail settings
            cls.MAIL_SERVER = config.get('mail', 'MAIL_SERVER')
            cls.MAIL_PORT = config.getint('mail', 'MAIL_PORT')
            cls.MAIL_USE_TLS = config.getboolean('mail', 'MAIL_USE_TLS')
            cls.MAIL_USE_SSL = config.getboolean('mail', 'MAIL_USE_SSL')

            # mail authentication and sender
            cls.MAIL_USERNAME = config.get('mail', 'MAIL_USERNAME')
            cls.MAIL_PASSWORD = config.get('mail', 'MAIL_PASSWORD')
            cls.MAIL_DEFAULT_SENDER = config.get('mail', 'MAIL_DEFAULT_SENDER')

            # Opalstack
            cls.OPALSTACK_API_TOKEN = config.get('opalstack', 'OPALSTACK_API_TOKEN')

class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    DEBUG = True
    WTF_CSRF_ENABLED = False
    DEBUG_TB_ENABLED = True

# dev config file at ./project/config/dev.cfg
DevelopmentConfig.load_config_file(os.path.join(basedir, 'config', 'dev.cfg'))


class TestingConfig(BaseConfig):
    """Testing configuration."""
    LOGIN_DISABLED=False
    TESTING = True
    DEBUG = False
    BCRYPT_LOG_ROUNDS = 1
    WTF_CSRF_ENABLED = False
    DEBUG_TB_ENABLED = False


class ProductionConfig(BaseConfig):
    """Production configuration."""
    DEBUG = False
    DEBUG_TB_ENABLED = False

    SECRET_KEY = None
    SECURITY_PASSWORD_SALT = None

# production config file at ./project/config/production.cfg
ProductionConfig.load_config_file(os.path.join(basedir, 'config', 'production.cfg'))
