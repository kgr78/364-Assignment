class RIPProtocol:
    def __init__(self, router_id, input_ports, outputs):
        self._router_id = router_id
        self._input_ports = input_ports
        self._outputs_ports = outputs
        # Set Up
        print("##################################{input_ports}##################################".format(input_ports=input_ports))
        self.init_Router_Interface(input_ports)

    def get_router_id(self):
        return self.router_id

    def get_input_ports(self):
        return self.input_ports

    def get_outputs(self):
        return self.outputs