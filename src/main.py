from configReader import *
from ripprotocol import RIPProtocol
import sys


def run_checks_and_get_values(config_file):
    parser = ConfigReader()
    parser.parseConfigFile(config_file)
    parser.validateConfig()

    router_id = parser.getRouterId()
    input_ports = parser.getInputPorts()
    outputs = parser.getOutputs()

    return router_id, input_ports, outputs


def main():
    if len(sys.argv) != 1:
        print("Usage: python main.py")
        sys.exit(1)

    num_routers = 7
    config_files = []
    for i in range(1, num_routers + 1):
        config_file = input(f"Enter config file name for router {i}: ")
        config_files.append(config_file)

    print("\nChecking configurations...\n")
    router_info = {}
    for config_file in config_files:
        try:
            router_id, input_ports, outputs = run_checks_and_get_values(config_file)
            router_info[router_id] = {'input_ports': input_ports, 'outputs': outputs}
            router = RIPProtocol(router_id, input_ports, outputs)
        except FileNotFoundError:
            print(f"Error: Configuration file '{config_file}' not found.")
            sys.exit(1)
        except KeyboardInterrupt:
            print("\nProgram terminated by user.")
            sys.exit(1)

if __name__ == "__main__":
    main()
