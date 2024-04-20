import unittest
from ConfigParser import ConfigParser
from RipProtocol import RipRouter


class TestRipRouter(unittest.TestCase):

    def setUp(self):
        # Set up router with a sample configuration file
        self.router = RipRouter("config1.txt")

    def tearDown(self):
        # Close sockets to avoid ResourceWarning
        self.router.close_input_sockets()

    def test_create_rip_packet(self):
        # Test create_rip_packet method
        message = self.router.create_rip_packet()
        self.assertIsInstance(message, bytearray)
        self.assertNotEqual(len(message), 0)

    def test_router_initialization(self):
        # Check router ID, input ports, and outputs after initialization
        self.assertEqual(self.router.router_id, 1)
        self.assertListEqual(self.router.input_ports, [5000, 5001, 5002])
        self.assertListEqual(self.router.output_ports, [5003, 5004, 5005])
        self.assertEqual(len(self.router.routing_table.routes), 0)


if __name__ == '__main__':
    unittest.main()
