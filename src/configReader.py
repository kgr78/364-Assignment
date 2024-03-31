class ConfigReader:
    def __init__(self):
        self.config = {}

    def parseConfigFile(self, filename):
        try:
            with open(filename, 'r') as file:
                for line in file:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        key, value = line.split(maxsplit=1)
                        self.config[key] = value
        except FileNotFoundError:
            print(f"Error: Configuration file '{filename}' not found.")
            exit(1)

    def validateConfig(self):
        required_params = ['router-id', 'input-ports', 'outputs']
        for param in required_params:
            if param not in self.config:
                print(f"Error: '{param}' parameter missing in the configuration file.")
                exit(1)

        if 'router-id' in self.config:
            try:
                router_id = int(self.config['router-id'])
                if router_id < 1 or router_id > 64000:
                    raise ValueError("Router ID must be between 1 and 64000.")
            except ValueError:
                print("Error: 'router-id' must be a positive integer between 1 and 64000.")
                exit(1)

        if 'input-ports' in self.config:
            input_ports = self.config['input-ports'].split(',')
            for port in input_ports:
                try:
                    port_num = int(port.strip())
                    if port_num < 1024 or port_num > 64000:
                        raise ValueError("Input port number must be between 1024 and 64000.")
                except ValueError:
                    print("Error: Input port numbers must be positive integers between 1024 and 64000.")
                    exit(1)

        if 'outputs' in self.config:
            outputs = self.config['outputs'].split(',')
            for output in outputs:
                port, metric, router_id = output.split('-')
                try:
                    port_num = int(port.strip())
                    metric_val = int(metric.strip())
                    router_id_val = int(router_id.strip())
                    if port_num < 1024 or port_num > 64000:
                        raise ValueError("Output port number must be between 1024 and 64000.")
                    if metric_val < 1:
                        raise ValueError("Metric value must be a positive integer.")
                    if router_id_val < 1 or router_id_val > 64000:
                        raise ValueError("Router ID in outputs must be between 1 and 64000.")
                except ValueError:
                    print("Error: Invalid format for output entry in the configuration file.")
                    exit(1)

    def getRouterId(self):
        return int(self.config['router-id'])

    def getInputPorts(self):
        input_ports = self.config['input-ports'].split(',')
        return [int(port.strip()) for port in input_ports]

    def getOutputs(self):
        outputs = self.config['outputs'].split(',')
        result = []
        for output in outputs:
            port, metric, router_id = output.split('-')
            result.append((int(port), int(metric), int(router_id)))
        return result
