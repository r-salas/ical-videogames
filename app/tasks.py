#
#
#   Jobs
#
#

import os
import pickle
import shutil
import tempfile
import datetime

from flask import current_app as app

from .data import Platform
from .extensions import scheduler
from .wikiparser import iterate_games


@scheduler.task("interval", id="fetch-game-releases", hours=24)
def update_game_releases():
    print("Populating game releases. This may take a while ...")

    with scheduler.app.app_context():
        os.makedirs(app.config["GAMES_DATA_DIR"], exist_ok=True)

    today = datetime.datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
    min_date = today - datetime.timedelta(days=60)
    max_date = today + datetime.timedelta(days=60)

    for platform in Platform:
        tracked_games_by_region = {
            "pal": [],
            "jp": [],
            "na": []
        }

        for game in iterate_games([platform]):
            for region in tracked_games_by_region.keys():
                release_date = getattr(game.release_date, region)

                if release_date is None or release_date < min_date or release_date > max_date:
                    continue

                tracked_games_by_region[region].append(game)

        # Save to file
        for region, tracked_games in tracked_games_by_region.items():
            fname = f"{platform.value}-{region}.pkl"

            with tempfile.NamedTemporaryFile(mode="wb", suffix=".pkl") as temp, scheduler.app.app_context():
                pickle.dump(tracked_games, temp)
                shutil.copy2(temp.name, os.path.join(app.config["GAMES_DATA_DIR"], fname))

    print("Game releases populated. All set ...")
