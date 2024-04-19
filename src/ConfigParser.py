from Router import Router

class ConfigParser:
    def __init__(self):
        self.router = Router()
       
    def validate_config(self, config_data):
        if len(config_data) != 3:
            raise ValueError("Config format is invalid. Each of 'router-id', 'input-ports', and 'outputs' must be specified on separate lines.")

        headers = [item[0][0] for item in config_data]
        if len(set(headers)) != len(headers):
            raise ValueError("Duplicate config headers found. Each header must be unique.")

    def validate_router_id(self, router_id_data, line_num):
        if len(router_id_data) != 2:
            raise ValueError(f"At line {line_num}, the router ID format is incorrect. Use 'router-id, {{integer between 1 and 64000}}'")

        try:
            router_id = int(router_id_data[1])
            if not (1 <= router_id <= 64000):
                raise ValueError(f"At line {line_num}, the router ID is invalid. It must be an integer between 1 and 64000.")
        except ValueError:
            raise ValueError(f"At line {line_num}, the router ID is invalid. It must be an integer.")
        self.router.set_router_id(router_id)
 
    def validate_input_ports(self, input_ports_data, line_num):
        try:
            for port_index, port_str in enumerate(input_ports_data[1:], start=1):
                port = int(port_str)
                if not (1024 <= port <= 64000):
                    raise ValueError(f"At line {line_num}, the input port number is invalid. Port {port_index} must be between 1024 and 64000.")
                if port in self.router.get_input_ports():
                    raise ValueError(f"At line {line_num}, a duplicate input port number is found. Port {port_index} is repeated.")
                self.router.add_input_port(port)
  
        except ValueError:
            raise ValueError(f"At line {line_num}, the input port number is invalid. Port {port_index} must be an integer.")

    def validate_output_links(self, outputs_data, line_num):
        for port_index, port_str in enumerate(outputs_data[1:], start=1):
            try:
                port, metric, router_id = map(int, port_str.split("-"))
            except ValueError:
                raise ValueError(f"At line {line_num}, the output format is invalid. Expected 'port-metric-router_id'.")

            if not (1024 <= port <= 64000):
                raise ValueError(f"At line {line_num}, the output port number is invalid. Port {port_index} must be between 1024 and 64000.")
            if router_id == self.router.router_id:
                raise ValueError(f"At line {line_num}, the output router ID is invalid. Router ID for port {port_index} must not be the same as the host router ID.")
            if port in self.router.get_outputs():
                raise ValueError(f"At line {line_num}, a duplicate output port number is found. Port {port_index} is repeated.")
            if port in self.router.input_ports:
                raise ValueError(f"At line {line_num}, the output port number is also used as an input port.")

            self.router.add_output(port, metric, router_id)

    def read_config_file(self, file_name):
        try:
            with open(file_name, 'r') as config_file:
                config = config_file.readlines()
        except FileNotFoundError:
            print(f"Error: The configuration file '{file_name}' was not found.")
            return
        parse_config = []
        for line_num, line in enumerate(config, start=1):
            line = line.strip()  # Remove leading/trailing spaces
            if line:
                parse_config.append((line.split(', '), line_num))

        self.validate_config(parse_config)
        
        for header, line_num in parse_config:
            if header[0] == 'router-id':
                self.validate_router_id(header, line_num)
            elif header[0] == 'input-ports':
                self.validate_input_ports(header, line_num)
            elif header[0] == 'outputs':
                self.validate_output_links(header, line_num)
            else:
                raise ValueError(f"At line {line_num}, the header '{header[0]}' is invalid.")
       
        return self.router
