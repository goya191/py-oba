#OneBusAawy app and testing

"""
Only checks 4 stops or so, all hardcoded.
"""

import datetime

import timeit


#3rd party - xmltodict
import xmltodict
import pprint

import query
from query import get_sched_url, make_request
import formatters
#
# keywords
#
ROUTE_ID = 'routeId'
BUS = "Route 36"
LINK = "link"
# Stop Locations
HOME_TO_WORK = "home_to_work"
WORK_TO_HOME = "work_to_home"

stops = {
    HOME_TO_WORK : {BUS : '1_3500', LINK : '1_99240'},
    WORK_TO_HOME : {BUS : '1_1530', LINK : '1_621'}
}
routes = {
    HOME_TO_WORK : {BUS : '1_100210', LINK : '40_100479'},
    WORK_TO_HOME : {BUS : '', LINK : ''}
}

DEFAULT_ROUTE_KEYS = \
    ('predictedArrivalTime','predictedDepartureTime',
     'scheduledArrivalTime', 'scheduledDepartureTime',
     'routeShortName' )

SPECIAL_KEY_ACTION = {
    "predictedArrivalTime" : query.ts_to_isoformat,
    "predictedDepartureTime" : query.ts_to_isoformat,
    "scheduledArrivalTime" : query.ts_to_isoformat,
    "scheduledDepartureTime" : query.ts_to_isoformat
}


def get_arriv_for_stop(stop_id):
    url = query.get_arr_url(stop_id)
    data = query.make_request(url)
    return data

# s['entry']['stopRouteSchedules']['stopRouteSchedule'][u'stopRouteDirectionSchedules']['stopRouteDirectionSchedule']['scheduleStopTimes']['scheduleStopTime']
def get_sched_for_stop(stop_id):
    url = query.get_sched_url(stop_id)
    data = query.make_request(url)
    return data

def filter_down_routes(route, keys=DEFAULT_ROUTE_KEYS, special_actions=SPECIAL_KEY_ACTION):
   filtered_routes = {}
   for k in keys:
       if route.has_key(k):
           temp = (route[k] if k not in special_actions else special_actions[k](route[k]))
           filtered_routes[k] = temp
   return filtered_routes

def route_to_string(route, keys=DEFAULT_ROUTE_KEYS, special_actions=SPECIAL_KEY_ACTION):
    route_strs = []
    for k in keys:
        if route.has_key(k):
            temp = (route[k] if k not in special_actions else special_actions[k](route[k]))
            route_strs.append(temp)
    return route_strs

    #item = [{route_key : route[route_key]} for route_key in display_keys if k route.has_key(k)]

def routes_to_string(route_list, keys=DEFAULT_ROUTE_KEYS, special_actions=SPECIAL_KEY_ACTION):
    """
    :param route_list:
    :param keys:
    :param special_actions: - dictionary of key to special key actions
        {keyname : function pointer}
    :return:
        list of strings
    """
    str_list = []
    for route in route_list:
        str_list.append(route_to_string(route=route, keys=keys, special_actions=special_actions))
    return tuple(str_list)


def find_next_arrival(stop_id, route_id):
    """
    HELPER

    :param stop_id: ID of the stop
    :param route_id:  ID of route
    :return: Tuple of times.
    """
    stop_id = stops[HOME_TO_WORK][BUS]
    data = get_arriv_for_stop(stop_id)
    #XXX hack, to work around xml parse or inconsistent response from OBA library
    arrivals = None
    if data.has_key('entry'):
        arrivals = data['entry']['arrivalsAndDepartures']['arrivalAndDeparture']
    elif data.has_key('arrivalsAndDepartures'):
        arrivals = data['arrivalsAndDepartures']['arrivalAndDeparture']
    else:
        raise ValueError("Expected key not present from One bus response!" )
    #[(x, y) for x in [1,2,3] for y in [3,1,4] if x != y]
    filtered_routes = [route for route in arrivals if route[ROUTE_ID] == route_id ]
    return filtered_routes


def get_next_two_arriv(arriv_info):
    now = datetime.datetime.now()

# TODO: 
# upcoming_time=datetime.timedelta(minutes=30), prev_time=datetime.timedelta(minutes=5)):
# def close_to_time(dt_li, spec_time=datetime.datetime.now(), 
#     close_to=datetime.timedelta(minutes=30)):
#     new_li = []
#     for dt_item in dt_li:
#         if abs(dt_item - spec_time) <= close_to:
#             new_li.append(dt_item)
#     return new_li

def close_to_time(dt_li, spec_time=datetime.datetime.now(), 
    close_to=datetime.timedelta(minutes=30)):
    new_li = []
    for dt_item in dt_li:
        diff = dt_item - spec_time
        if diff >= datetime.timedelta(seconds=0) and diff <= close_to:
        #if dt_item - spec_time <= close_to:
            new_li.append(dt_item)
    return new_li

def get_sched_arriv_dts(stop_id):
    """
    Entire Link operation query
    """
    now = datetime.datetime.now()
    qr = get_sched_for_stop(stop_id)
    #filter! 
    arriv_dts = query.query_to_dts(qr)
    return close_to_time(arriv_dts)
    # incomplete

#
# Full functions
#
def full_next_arriv(route_id, stop_id):
    # list of dicts
    filtered_route_info = find_next_arrival(route_id=route_id, stop_id=stop_id)
    # XXX avoid this:
    predicted_times = []
    for f in filtered_route_info:
        temp = f['predictedArrivalTime']
        predicted_times.append(query.ts_to_dt(temp))
    formatters.print_py_dt_list(predicted_times, title="Route 36")

def full_schedule(stop_id):
    res = get_sched_arriv_dts(stop_id)
    #print formatters.SEP
    formatters.print_py_dt_list(res, "LINK light rail")

def main():
    now = datetime.datetime.now()
    formatters.print_py_dt_list([now], "Current time")
    # get route 36
    rt_36_stop = stops[HOME_TO_WORK][BUS]
    rt_36_id = routes[HOME_TO_WORK][BUS]
    full_next_arriv(route_id=rt_36_id, stop_id=rt_36_stop)

    # get LINK schedule
    link_stop = stops[HOME_TO_WORK][LINK]
    full_schedule(stop_id=link_stop)

if __name__ == "__main__":
    import pdb, traceback, sys
    try:
        main()
    except:
        type, value, tb = sys.exc_info()
        traceback.print_exc()
        pdb.post_mortem(tb)
