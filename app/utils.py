#
#
#   Utils
#
#

import os
import datetime
import dateutil.parser

from typing import Optional


def safe_parse_datetime(s) -> Optional[datetime.datetime]:
    """Returns None if strptime fails"""
    try:
        return dateutil.parser.parse(s)
    except dateutil.parser.ParserError:
        return None


def is_flask_debug_mode():
    """Get app debug status."""
    debug = os.environ.get("FLASK_DEBUG")
    if not debug:
        return os.environ.get("FLASK_ENV") == "development"
    return debug.lower() not in ("0", "false", "no")


def is_werkzeug_reloader_process():
    """Get werkzeug status."""
    return os.environ.get("WERKZEUG_RUN_MAIN") == "true"
