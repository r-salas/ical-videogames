#
#
#   App
#
#

import datetime

from flask import Flask

from . import routes
from .config import Config
from .extensions import scheduler
from .utils import is_flask_debug_mode, is_werkzeug_reloader_process


def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static", static_url_path="/static")

    app.config.from_object(Config)

    scheduler.init_app(app)

    app.register_blueprint(routes.blueprint)

    with app.app_context():
        if is_flask_debug_mode() and not is_werkzeug_reloader_process():
            pass  # Prevent scheduler to run twice
        else:
            from . import tasks

            if app.config["POPULATE_ON_STARTUP"]:
                for job in scheduler.get_jobs():
                    job.modify(next_run_time=datetime.datetime.now())

            scheduler.start()

    return app
