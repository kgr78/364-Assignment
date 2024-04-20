import unittest
from ConfigParser import ConfigParser

class TestConfigParser(unittest.TestCase):
    def test_valid_config(self):
        print("Testing valid configuration...")
        config_parser = ConfigParser()
        router = config_parser.read_config_data([
            "router-id, 1",
            "input-ports, 5000, 5001, 5002",
            "outputs, 5003-1-2, 5004-5-6, 5005-8-7"
        ])
        self.assertEqual(router.get_router_id(), 1)
        self.assertEqual(router.get_input_ports(), [5000, 5001, 5002])
        self.assertEqual(router.get_outputs(), [5003, 5004, 5005]) 
        print("Valid configuration test passed.")

    def test_invalid_config(self):
        print("Testing invalid configuration...")
        invalid_config_data = [
            "router-id, 1",
            "input-ports, 5000, 5001, 5002",
            "outputs, 5003-1-2, 5004-5-6, 5005-8-7",
            "invalid-section, data" 
        ]

        config_parser = ConfigParser()
        with self.assertRaises(ValueError):
            router = config_parser.read_config_data(invalid_config_data)

        print("Invalid configuration test passed.")

    def test_duplicate_entries(self):
        print("Testing duplicate entries...")
        duplicate_config_data = [
            "router-id, 1",
            "input-ports, 5000, 5001, 5002",
            "outputs, 5003-1-2, 5004-5-6, 5005-8-7",
            "outputs, 5006-4-3, 5007-7-9"
        ]

        config_parser = ConfigParser()
        with self.assertRaises(ValueError):
            router = config_parser.read_config_data(duplicate_config_data)
        print("Duplicate entries test passed.")

if __name__ == '__main__':
    unittest.main()
