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

    def test_get_arriv_for_stop(self):
        stop_id = stops[HOME_TO_WORK][BUS]
        data = OBA.get_arriv_for_stop(stop_id)
        assert(data)

if __name__ == "__main__":
    unittest.main()
