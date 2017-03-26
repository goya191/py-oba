#OneBusAawy app and testing

"""
Only checks 4 stops or so, all hardcoded.
"""

import datetime

import timeit

import pdb

#3rd party - xmltodict
import xmltodict
import pprint

import query
from query import make_request
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

def get_arriv_for_stop(stop_id):
    url = query.get_arr_url(stop_id)
    data = query.make_request(url)
    return data



    #item = [{route_key : route[route_key]} for route_key in display_keys if k route.has_key(k)]


def find_next_arrival(stop_id, route_id):
    """
    HELPER

    :param stop_id: ID of the stop
    :param route_id:  ID of route
    :return: Tuple of times.
    """
    data = get_arriv_for_stop(stop_id)
    # hack to work around xml parse or inconsistent response from OBA library
    arrivals = None
    if data.has_key('entry'):
        arrivals = data['entry']['arrivalsAndDepartures']['arrivalAndDeparture']
    elif data.has_key('arrivalsAndDepartures'):
        arrivals = data['arrivalsAndDepartures']['arrivalAndDeparture']
    else:
        raise ValueError("Expected key not present from One bus response!" )
    # filter by route id
    filtered_routes = [route for route in arrivals if route[ROUTE_ID] == route_id ]
    # take out invalid date
    #raise ValueError('test')
    filtered_routes = [route for route in filtered_routes if route.get('predictedArrivalTime') != u'0']
    return filtered_routes


def get_sched_arriv_dts(stop_id):
    """
    Entire Link operation query
    """
    now = datetime.datetime.now()
    qr = get_sched_for_stop(stop_id)
    #filter! 
    arriv_dts = query.query_to_dts(qr)
    return close_to_time(arriv_dts)


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
    return predicted_times

"""
Special purpose helper functions - get one route each
"""

def get_bus():
    rt_36_stop = stops[HOME_TO_WORK][BUS]
    rt_36_id = routes[HOME_TO_WORK][BUS]
    return full_next_arriv(route_id=rt_36_id, stop_id=rt_36_stop)

def get_link():
    link_stop = stops[HOME_TO_WORK][LINK]
    link_route = routes[HOME_TO_WORK][LINK]
    return full_next_arriv(route_id=link_route, stop_id=link_stop)

def main():
    now = datetime.datetime.now()
    print formatters.fmt_py_dt_list([now], "Current time")

    bus_rounte_info = get_bus()
    print formatters.fmt_py_dt_list(bus_rounte_info, title="Route 36")
    link_route_info = get_link()
    print formatters.fmt_py_dt_list(link_route_info, title="LINK light rail")


if __name__ == "__main__":
    import pdb, traceback, sys
    try:
        main()
    except:
        type, value, tb = sys.exc_info()
        traceback.print_exc()
        pdb.post_mortem(tb)
