#
#
#   App
#
#

from flask import Flask

from . import routes
from .config import Config
from .extensions import scheduler
from .utils import is_flask_debug_mode, is_werkzeug_reloader_process


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    scheduler.init_app(app)

    app.register_blueprint(routes.blueprint)

    with app.app_context():
        if is_flask_debug_mode() and not is_werkzeug_reloader_process():
            pass  # Prevent scheduler to run twice
        else:
            from . import tasks

            print("Populating game releases. This may take a while ...")
            tasks.update_game_releases()
            print("Game releases populated. All set ...")

            scheduler.start()

    return app
