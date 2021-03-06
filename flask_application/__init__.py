import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask

FLASK_APP_DIR = os.path.dirname(os.path.abspath(__file__))


app = Flask(
    __name__,
    template_folder=os.path.join(FLASK_APP_DIR, '..', 'templates'),
    static_folder=os.path.join(FLASK_APP_DIR, '..', 'static')
)

#  Config
app.config.from_object('flask_application.config.app_config')
app.logger.info("Config: %s" % app.config['ENVIRONMENT'])

#  Logging
import logging
logging.basicConfig(
    level=app.config['LOG_LEVEL'],
    format='%(asctime)s %(levelname)s: %(message)s '
           '[in %(pathname)s:%(lineno)d]',
    datefmt='%Y%m%d-%H:%M%p',
)

#  Email on errors
if not app.debug and not app.testing:
    import logging.handlers
    mail_handler = logging.handlers.SMTPHandler(
        'localhost',
        os.getenv('USER'),
        app.config['SYS_ADMINS'],
        '{0} error'.format(app.config['SITE_NAME']),
    )
    mail_handler.setFormatter(logging.Formatter('''
        Message type:       %(levelname)s
        Location:           %(pathname)s:%(lineno)d
        Module:             %(module)s
        Function:           %(funcName)s
        Time:               %(asctime)s

        Message:

        %(message)s
    '''.strip()))
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)
    app.logger.info("Emailing on error is ENABLED")
else:
    app.logger.info("Emailing on error is DISABLED")

# Bootstrap
from flask_bootstrap import Bootstrap
Bootstrap(app)

# Assets
from flask.ext.assets import Environment
assets = Environment(app)
# Ensure output directory exists
assets_output_dir = os.path.join(FLASK_APP_DIR, '..', 'static', 'gen')
if not os.path.exists(assets_output_dir):
    os.mkdir(assets_output_dir)

# Email
from flask.ext.mail import Mail
mail = Mail(app)

# Memcache
from flask.ext.cache import Cache
app.cache = Cache(app)

# Business Logic
# http://flask.pocoo.org/docs/patterns/packages/
# http://flask.pocoo.org/docs/blueprints/
from flask_application.controllers.frontend import frontend
app.register_blueprint(frontend)

# MongoEngine
from flask.ext.mongoengine import MongoEngine
app.db = MongoEngine(app)

from flask.ext.security import Security, MongoEngineUserDatastore
from flask_application.models import User, Role

# Setup Flask-Security
user_datastore = MongoEngineUserDatastore(app.db, User, Role)
app.security = Security(app, user_datastore)

from flask_application.controllers.admin import admin
app.register_blueprint(admin)

