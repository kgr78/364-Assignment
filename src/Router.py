class Router:

    def __init__(self):
        self.outputs = []
        self.router_id = None
        self.input_ports = []
    def add_input_port(self, port):
        self.input_ports.append(port)
    def get_input_ports(self):
        return self.input_ports
    def set_router_id(self, router_id):
        self.router_id = router_id
    def get_router_id(self):
        return self.router_id
    def create_output(self, port, metric, router_id):
        return {
            'port': port,
            'metric': metric,
            'router_id': router_id
        }

    def add_output(self, port, metric, router_id):

        self.outputs.append(self.create_output(port, metric, router_id))
    
    def get_output_by_router_id(self, router_id):
       
        for output in self.outputs:
            if output['router_id'] == router_id:
                return output

    def get_outputs(self):
       
        return [output['port'] for output in self.outputs]

    def is_router_in_outputs(self, router_id):
      
        return router_id in [output['router_id'] for output in self.outputs]

    def print_outputs(self):
    
        for output in self.outputs:
            print(output)
