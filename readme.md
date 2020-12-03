# OpalStack Mailbox Change Password

A simple flask app that uses tokens and email confirmation to 
allow users to change their own email password on Opalstack.

Goal: simple to install / configure / use.  No DB or media required.

## QuickStart for install on Opalstack

1. create Python app, say named `pwdch` (https://help.opalstack.com/article/60/pythonuwsgi-applications)
```sh
$ git clone https://github.com/powderflask/opalstack-pwdch.git ~/apps/pwdch/src
$ source ~/apps/pwdch/env/bin/activate
$ pip install -r ~/apps/pwdch/src/requirements.txt
```

2. edit `~/apps/pwdch/uwsgi.ini`  (https://help.opalstack.com/article/60/pythonuwsgi-applications)
```sh
pythonpath = /home/<you>/apps/pwdch/src
module = project:app
touch-reload = /home/<you>/apps/pwdch/src/project/__init__.py

env = FLASK_APP=project
env = APP_SETTINGS=project.config.ProductionConfig
```

3. Configure your secrets and app settings (see below), then restart your app:
```shell script
$ ~/apps/pwdch/stop
$ ~/apps/pwdch/start
```


### Configure with .cfg file
```sh
$ cp project/config/production.cfg.sample project/config/production.cfg
```  
  - configures secrets and email settings for `project.config.ProductionConfig`
  
### Configure via Environment Variables

Development Example (with [Debug Mail](https://debugmail.io)):

```sh
$ export APP_SETTINGS="project.config.DevelopmentConfig"
$ export APP_MAIL_SERVER=debugmail.io
$ export APP_MAIL_PORT=25
$ export APP_MAIL_USE_TLS=true
$ export APP_MAIL_USE_SSL=false
$ export APP_MAIL_USERNAME=ADDYOUROWN
$ export APP_MAIL_PASSWORD=ADDYOUROWN
$ export APP_OPALSTACK_API_TOKEN=YOURAPITOKEN
```

Production Example:

```sh
$ export APP_SETTINGS="project.config.ProductionConfig"
$ export APP_MAIL_SERVER=ADDYOUROWN
$ export APP_MAIL_PORT=587
$ export APP_MAIL_USE_TLS=true
$ export APP_MAIL_USE_SSL=true
$ export APP_MAIL_USERNAME=ADDYOUROWN
$ export APP_MAIL_PASSWORD=ADDYOUROWN
$ export APP_OPALSTACK_API_TOKEN=YOURAPITOKEN
```

## Misc

### Clean environment

```sh
sh clean.sh
```

### Run dev server

```sh
$ flask run
```

### Tests  ** NEED TO BE MOCKED **

Without coverage:

```sh
$ python manage.py test
```

With coverage:

```sh
$ python manage.py cov
```

## How does it work?

1. User enters their email and mailbox username
    - app verifies both are valid on your Opalstack account 
        - and that the mailbox is set as a destination for the email address (verify email and mailuser are linked)
    - app encrypts the mailbox name in a time-stamped token and emails a link containing token to user
2. User receives link by email and clicks link, thus returning the token to the app.
    - app decodes token to get mailuser, verifying token was returned before it expires
3. User enters and confirms password
    - app attempts to update password at Opalstack (assumes password is too simple if attempt fails)
    - if successful, user is directed to verify their new password by logging in to webmail.opalstack.com
    
### Caveats

Since this tool never verifies the end-user had the original mailbox password, there may be edge cases where a user
is able to change the password for a mailbox they did not previously have the password for.

For example, the approach used here makes a big assumption that a user who controls an email also 
controls any mailbox that email is a destination for.
    - While this is often true, in cases where multiple mailboxes or a mailbox and forwarders are configured on a 
     single email, it is possible some recipients who should not have control over the mailbox will recieve
     the password reset link.

## Credits

Based on an old tutorial at RealPython.com:  https://realpython.com/handling-email-confirmation-in-flask/

This is my first Flask app - please excuse if I'm not following conventions.
