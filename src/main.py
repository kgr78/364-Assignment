from configReader import ConfigReader
import sys


def get_config_file():
    config_file = input("Enter the configuration file name: ")
    return config_file


def run_checks_and_get_values():
    config_file = get_config_file()

    parser = ConfigReader()
    parser.parseConfigFile(config_file)
    parser.validateConfig()

    router_id = parser.getRouterId()
    input_ports = parser.getInputPorts()
    outputs = parser.getOutputs()

    return router_id, input_ports, outputs


def main():
    try:
        router_id, input_ports, outputs = run_checks_and_get_values()
        print(f"Router ID: {router_id}")
        print(f"Input Ports: {input_ports}")
        print(f"Outputs: {outputs}")
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
        sys.exit(1)


if __name__ == "__main__":
    main()
