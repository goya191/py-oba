#OneBusAawy app and testing

"""
Only checks 4 stops or so, all hardcoded.
"""

import datetime

import time
import timeit

import urllib2
import urlparse

#3rd party - xmltodict
import xmltodict
import urlparse

"""
Example queries
http://api.pugetsound.onebusaway.org/api/where/schedule-for-stop/1_3500.xml?key=TEST&route=1_100210
"""

BASE_API = "http://api.pugetsound.onebusaway.org/api/"
BASE_Q_STRING = "?key=TEST"
#BASE_API_REQ = BASE_API + "/{0}/{1}/{2}.xml?key=TEST"

#API commands
SCHED_FOR_STOP = "where/schedule-for-stop/{}.xml"
AR_FOR_STOP = "where/arrivals-and-departures-for-stop/{stop_id}.xml"


def get_sched_url(stop_name):
    return urlparse.urljoin(
        urlparse.urljoin(
            BASE_API, SCHED_FOR_STOP.format(stop_name)), BASE_Q_STRING)

def get_arr_url(stop_id):
    """
    id - the stop id, encoded directly in the url:
    http://api.pugetsound.onebusaway.org/api/where/arrivals-and-departures-for-stop/[ID GOES HERE].xml
    minutesBefore=n - include vehicles having arrived or departed in the previous n minutes (default=5)
    minutesAfter=n - include vehicles arriving or departing in the next n minutes (default=35)

    time - by default, the method returns the status of the system right now. However, the system can also be queried at a specific time.
    This can be useful for testing. See timestamps for details on the format of the time parameter.

    :param stop_id:
    :return:
    """
    return urlparse.urljoin(
        urlparse.urljoin(
            BASE_API, AR_FOR_STOP.format(stop_id=stop_id)), BASE_Q_STRING)
#'http://api.pugetsound.onebusaway.org/api/where/arrivals-and-departures-for-stop/1_3500.xml?key=TEST'


#http://api.pugetsound.onebusaway.org/api/where/schedule-for-stop/1_99240.xml?key=TEST
#
# OBA API calls
#
def send_request(query_str):
    """
    Attempts request, catches recoverable error, 
    returns error or successful object request
    """
    req = None
    try:
        req = urllib2.urlopen(query_str)
    except urllib2.URLError as e:
         return e.code
    return req
    

def make_request(query_str, tries=3):
    """
    attempt up to # of tries to contact OBA api
    raise IOError if fail
    """
    if tries == 0:
        raise IOError("exceeded tries in make_request")
    req = send_request(query_str)
    if type(req) == int:
        # the request failed for some reason
        if req == 429:
            # retry recoverable error, make recursive call
            time.sleep(0.1)
            return make_request(query_str, tries - 1 )

    http_code = req.getcode()
    
    if http_code == 200:
        return parse_xml(req.read())
    else:
        raise ValueError("URL request on {}\n status: {} - {}" (query_str, req.getcode(), req.msg))
    # should not get here
    raise RuntimeError("unexpected path from make_requst!")
    

    
    
def parse_xml(xml_data):
    """
    uses library, ignores 'response'
    XXX error handling ?
    """
    return xmltodict.parse(xml_data)['response']['data']


def parse_arival_time(stop_time_dict):
    return ts_to_dt(stop_time_dict['arrivalTime'])


#
# Filtering
#

def key_from_list(li, key):
    """
    Returns the specified key out of the list of dicts 
    """
    new_list = []
    for dict_item in li:
        temp = dict_item.get(key)
        if temp is not None:
            new_list.append(temp)
    return new_list

def filter_sched_for_stop(stop_dict):
    return stop_dict['entry']['stopRouteSchedules']['stopRouteSchedule'][u'stopRouteDirectionSchedules']['stopRouteDirectionSchedule']['scheduleStopTimes']['scheduleStopTime']

#
# Datetime
#

def ts_to_isoformat(ts):
    if ts == None or ts == 0:
        return None
    dt = ts_to_dt(ts)
    return dt.isoformat()
    

def dt_to_unix(dt):
    return unix_time(dt) * 1000.0

def ts_to_dt(ts):
    """
    XXX blind cast
    """
    return datetime.datetime.fromtimestamp(int(ts)/1000)


# List operations

def ts_list_to_dates(ts_list):
    new_li = []
    for item in ts_list:
        new_li.append(ts_to_dt(item))
    return new_li

#
# full operations
#
def query_to_dts(query_results):
    li = filter_sched_for_stop(query_results)
    ts_li = key_from_list(li, 'arrivalTime')
    return ts_list_to_dates(ts_li)