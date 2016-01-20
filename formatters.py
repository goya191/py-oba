import pprint

STRFTIME_TIME_STR_12 = "%I"
SEP = '=' * 80


def print_dt_iso(py_dt):
    pprint(py_dt.isoformat())

def build_time_str(py_dt):
    beg_str = py_dt.strftime("%I:%M")
    am_pm = "AM" if py_dt.hour <= 11 else "PM"
    return beg_str + " " + am_pm
# list operations

def print_py_dt_list(py_dt_list, title=None):
    if title is not None:
    	print SEP
        print title
        print SEP
    for py_dt in py_dt_list:
        pprint.pprint(build_time_str(py_dt))
