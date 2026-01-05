#
#
#   Utils
#
#

import os
import datetime

from typing import Optional, Union


def safe_strptime(s, pattern, date: bool = False) -> Optional[Union[datetime.datetime, datetime.date]]:
    """Returns None if strptime fails"""
    try:
        datetime_val = datetime.datetime.strptime(s, pattern)
        if date:
            return datetime_val.date()
        return datetime_val
    except ValueError:
        return None


def replace_short_month(s):
    month_dict = {
        "Jan ": "January ",
        "Feb ": "February ",
        "Mar ": "March ",
        "Apr ": "April ",
        "May ": "May ",
        "Jun ": "June ",
        "Jul ": "July ",
        "Aug ": "August ",
        "Sep ": "September ",
        "Sept ": "September ",
        "Oct ": "October ",
        "Nov ": "November ",
        "Dec ": "December "
    }

    for short_month, long_month in month_dict.items():
        s = s.replace(short_month, long_month)

    return s


def is_flask_debug_mode():
    """Get app debug status."""
    debug = os.environ.get("FLASK_DEBUG")
    if not debug:
        return os.environ.get("FLASK_ENV") == "development"
    return debug.lower() not in ("0", "false", "no")


def is_werkzeug_reloader_process():
    """Get werkzeug status."""
    return os.environ.get("WERKZEUG_RUN_MAIN") == "true"


def strtobool(v):
    return v.lower() in ("yes", "true", "t", "1")
