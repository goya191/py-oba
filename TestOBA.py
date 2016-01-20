import unittest
import pprint

import main
import main as OBA
from main import stops, routes
from main import HOME_TO_WORK, WORK_TO_HOME, BUS, LINK


"""
test cmd:
C:\Python27\Scripts\nosetests.exe --pdb
"""

TEST_STOP_ID = "1_3500"

class TestApi(unittest.TestCase):
    #
    # #TEST_QUERY_HOME = "http://api.pugetsound.onebusaway.org/api/where/stop/1_3500.xml?key=TEST&route=1_100210"
    # def test_make_req(self):
    #     
    #     url = OBA.get_sched_url(TEST_STOP_ID)
    #     print url
    #     data = OBA.make_request(url)
    #     assert False

    def test_get_stop_info(self):
        stop_id = stops[HOME_TO_WORK][BUS]
        data = OBA.get_stop_arrival_info(stop_id)
        assert(data)

    def test_get_arriv_for_stop(self):
        stop_id = stops[HOME_TO_WORK][BUS]
        data = OBA.get_arriv_for_stop(stop_id)
        assert(data)

    def test_get_times(self):
        route_id = routes[HOME_TO_WORK][BUS]
        stop_id = stops[HOME_TO_WORK][BUS]
        filtered_arr_info = OBA.find_next_arrival(route_id=route_id, stop_id=stop_id)
        #assert(filtered_arr_info)

    def test_get_route_strings(self):
       #get route
        route_id = routes[HOME_TO_WORK][BUS]
        stop_id = stops[HOME_TO_WORK][BUS]
        filtered_route_info = OBA.find_next_arrival(route_id=route_id, stop_id=stop_id)
        route_strings = OBA.routes_to_string(filtered_route_info)
        #pprint.pprint(route_strings)

    def test_get_route_strings_alt(self):
        route_id = routes[HOME_TO_WORK][LINK]
        stop_id = stops[HOME_TO_WORK][LINK]
        filtered_route_info = OBA.find_next_arrival(route_id=route_id, stop_id=stop_id)
        route_strings = OBA.routes_to_string(filtered_route_info)
        pprint.pprint(route_strings)        


if __name__ == "__main__":
    unittest.main()
