# OpalStack Mailbox Change Password

A simple flask app that uses tokens and email confirmation to 
allow users to change their own email password on Opalstack.

Goal: simple to install / configure / use.  No DB or media required.

## QuickStart for install on Opalstack

1. create Python app, say named `pwdch` (https://help.opalstack.com/article/60/pythonuwsgi-applications)
```sh
$ svn export https://github.com/powderflask/opalstack-pwdch.git/trunk ~/apps/pwdch/src
or
$ git clone https://github.com/powderflask/opalstack-pwdch.git ~/apps/pwdch/src

$ source ~/apps/pwdch/env/bin/activate
$ pip install -r ~/apps/pwdch/src/requirements.txt
$ ln -s ~/apps/pwdch/src/project ~/apps/pwdch
```

2. edit `~/apps/pwdch/uwsgi.ini`  (https://help.opalstack.com/article/60/pythonuwsgi-applications)
```sh
pythonpath = /home/<you>/apps/pwdch
module = project:app
touch-reload = /home/<you>/apps/pwdch/project/__init__.py

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

### Clean environment

```sh
sh clean.sh
```

### Run

```sh
$ python manage.py runserver
```

### Testing

Without coverage:

```sh
$ python manage.py test
```

With coverage:

```sh
$ python manage.py cov
```

### Credits

Based on an old tutorial at RealPython.com:  https://realpython.com/handling-email-confirmation-in-flask/

This is my first Flask app - please excuse if I'm not following conventions.
