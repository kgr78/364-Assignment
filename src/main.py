from configReader import *
from socketBinder import *
from ripProtocol import *

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

    config_files = []
    router_info = {}

    while True:
        config_file = input("Enter config file name (or 'q' to quit): ")
        if config_file.lower() == 'q':
            break
        config_files.append(config_file)

        try:
            router_id, input_ports, outputs = run_checks_and_get_values(config_file)
            router_info[router_id] = {'input_ports': input_ports, 'outputs': outputs}
            RouterInterface(input_ports)
            print(f"Router {router_id} input ports: {input_ports} bound successfully.")
        except FileNotFoundError:
            print(f"Error: Configuration file '{config_file}' not found.")
        except KeyboardInterrupt:
            print("\nProgram terminated by user.")
            sys.exit(1)
        except Exception as e:
            print(f"Error processing configuration file '{config_file}': {e}")

    # Start the RIPProtocol to listen for incoming data on input ports
    rip_protocol = RIPProtocol(router_info)
    rip_protocol.start_listening()


if __name__ == "__main__":
    main()
