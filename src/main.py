from configReader import *
from configReader import ConfigReader
from ripprotocol import RIPProtocol
import sys

def parse_inputs():
    """ Parsing and validating inputs"""
    if len(sys.argv) != 2:
        print("Error: You must input exactly one parameter which is the config file name, eg python3 main.py config1.txt")
        sys.exit()
    else:
        config_file = sys.argv[1]
    return config_file
# def get_config_file():
#     config_file = input("Enter the configuration file name: ")
#     return config_file


def run_checks_and_get_values(config_file):

    # config_file = get_config_file()
    parser = ConfigReader()
    parser.parseConfigFile(config_file)
    parser.validateConfig()

    router_id = parser.getRouterId()
    input_ports = parser.getInputPorts()
    outputs = parser.getOutputs()

    return router_id, input_ports, outputs


def main():
    """ Start function for RIP daemon"""
    try:
        config_file = parse_inputs()
    except ValueError as error:
        print("Error: ", error)
        return
    try:
        router_id, input_ports, outputs = run_checks_and_get_values(config_file)
        router = RIPProtocol(router_id, input_ports, outputs)
        print(f"Router ID: {router_id}")
        print(f"Input Ports: {input_ports}")
        print(f"Outputs: {outputs}")
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
        sys.exit(1)


# if __name__ == "__main__":
#     main()
main()
