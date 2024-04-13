from configReader import *
from ripRoute import Router
from socketBinder import *
from ripProtocol import *

import sys


def run_checks_and_get_values(config_file):
    parser = ConfigReader()
    config_checker = readConfigFile(config_file)
    # print(f"##################{config_checker}")
    data = parser.validateConfig(config_checker)
    print(f"##################{data}")
    return data


def create_router(data):
    router_id = data['router_id']
    input_ports = data['input_ports']
    outputs = data['outputs']
    router = Router(router_id, input_ports, outputs)
    print(f"Created Router {router.get_router_id()}")
    return router


def main():
    try:
        if len(sys.argv) != 2:
            raise ValueError("Invalid argument, usage: python3 main.py <config_file>")

        config_file = sys.argv[1]
    except ValueError as error:
        print(error)
        return

    router_info = {}
    print(config_file)
    try:
        print("#####")
        data = run_checks_and_get_values(config_file)
        print("#####")
        router = create_router(data)
        # router_info[router.get_router_id()] = {'input_ports': input_ports, 'outputs': outputs}
        RouterInterface(router._inputs)
        rip_protocol = RIPProtocol(router_info)
        rip_protocol.start_listening()
        print(f"Router {router.get_router_id()} input ports: {router.get_input_ports()} bound successfully.")
    except FileNotFoundError:
        print(f"Error: Configuration file '{config_file}' not found.")
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
        sys.exit(1)
    except Exception as e:
        print(f"Error processing configuration file '{config_file}': {e}")


if __name__ == "__main__":
    main()

