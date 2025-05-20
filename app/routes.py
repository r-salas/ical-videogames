#
#
#   Routes
#
#

import os
import pickle

from .data import Platform

from ics import Calendar, Event
from flask import Blueprint, request, Response, render_template, current_app as app


def _parse_region(region):
    region = region.lower()

    if region not in ("pal", "na", "jp"):
        raise ValueError("Unknown region")

    return region


def _parse_platform(label):
    return Platform(label)


def _platform_to_readable(platform):
    mapper = {
        Platform.PS5: "PS5",
        Platform.PC: "PC",
        Platform.PS4: "PS4",
        Platform.NINTENDO_SWITCH: "Nintendo Switch",
        Platform.NINTENDO_SWITCH_2: "Nintendo Switch 2",
        Platform.XBOX_ONE: "Xbox One",
        Platform.XBOX_SERIES: "Xbox Series X",
    }
    return mapper[platform]


blueprint = Blueprint("index", __name__)


@blueprint.route("/")
def index():
    return render_template("index.html")


@blueprint.route("/ping")
def ping():
    return "pong"


@blueprint.route("/calendar")
def calendar():
    platforms = request.args.getlist("platform", type=_parse_platform)
    region = request.args.get("region", default="pal", type=_parse_region)

    cal = Calendar()

    for platform in platforms:
        fname = f"{platform.value}-{region}.pkl"
        fpath = os.path.join(app.config["GAMES_DATA_DIR"], fname)

        try:
            with open(fpath, "rb") as fp:
                games = pickle.load(fp)
        except Exception as e:
            app.logger.exception(f"Error loading {fpath}")
            games = []

        for game in games:
            release_date = getattr(game.release_date, region)

            event = Event(name=f"{game.title} ({_platform_to_readable(game.platform)} version)", begin=release_date)
            event.make_all_day()

            cal.events.add(event)

    return Response(
        str(cal),
        mimetype="text/calendar",
        headers={
            "Content-disposition": "inline; filename=games.ics"
        }
    )
