import unittest
import datetime
from Route import Route
from RoutingTable import RoutingTable

class TestRoutingTable(unittest.TestCase):
    def setUp(self):
        self.routing_table = RoutingTable()
        self.routing_table.set_router_id("Router1")
        self.routing_table.add_route("Router2", "Router2", 1)
        self.routing_table.add_route("Router3", "Router2", 2)
        self.routing_table.add_route("Router4", "Router3", 3)

    def test_is_route_known(self):
        self.assertTrue(self.routing_table.is_route_known("Router2"))
        self.assertFalse(self.routing_table.is_route_known("Router5"))

    def test_get_route_id_by_id(self):
        route = self.routing_table.get_route_id_by_id("Router2")
        self.assertIsInstance(route, Route)
        self.assertEqual(route.destination, "Router2")
        self.assertEqual(route.next_hop, "Router2")
        self.assertEqual(route.metric, 1)

if __name__ == '__main__':
    unittest.main()