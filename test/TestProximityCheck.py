import unittest

class TestProximityCheck(unittest.TestCase):
    def test_check_proximity(self):
        order = {'delivery_address': "10 10"}
        warehouse = {'coordinates': "5 5"}
        self.assertTrue(self.check_proximity(order['delivery_address'], warehouse['coordinates']))
