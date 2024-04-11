import socket
import select

from ripRoute import Route


class RIPProtocol:
    def __init__(self, router_info):
        
        self.router_info = router_info
        self._routing_table = {}
        self.route = []
        self.init_routing_table()
        self.print_routing_table()
    def init_routing_table(self):
        route = Route(0, 0, None)
        self.route.append(route)
        print(self.route)
        router_id = next(iter(self.router_info))
        self._routing_table[router_id] = route
    def print_routing_table(self):
        print(f"Routing Table info:{self.router_info}")
        columns = "|   Destination   |   Next Hop  | Metric | Timeout  | Garbage Timer | State   |"
        print(columns)
        for i in self._routing_table.items():
            print(f"| {Route._destination} | {Route._next_hop} | {Route._metric} | {Route._deletion_timer} | {Route._garbage_timer} | {Route._state} |")
    
    def init_routing_table(self):
        for router_id, router_data in self.router_info.items():
            outputs = router_data['outputs']
            for output_port, metric, dest_router_id in outputs:
                self._routing_table[output_port] = {
                    'next': dest_router_id,
                    'timeout': None,
                    'state': 'active'
                }

    def start_listening(self):
        while True:
            for router_id, router_data in self.router_info.items():
                input_ports = router_data['input_ports']
                for input_port in input_ports:
                    self.receive_data(input_port)

    def receive_data(self, input_port):
        try:
            sock = self.router_info[input_port]['socket']  # Get the socket from RouterInterface
            readable_sockets, _, _ = select.select([sock], [], [], 1)  # Timeout of 1 second
            if readable_sockets:
                data, addr = sock.recvfrom(1024)
                print(f"Received data from {addr}: {data.decode('utf-8')}")
        except socket.error as e:
            print(f"Error receiving data on port {input_port}: {e}")

    def update_routing_table(self):
        pass
    def process_packet(self, data):
        pass

    def handle_timers(self):
        pass



    def send_data(self, output_port, data):
        pass
