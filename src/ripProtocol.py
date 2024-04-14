import socket
import select

from ripRoute import Router


# This creates the entry packet
def create_entry_packet(router_id, metric):
    address_family = 2
    entryPacket = bytearray([(address_family >> 8), (address_family & 0xFF), (0 >> 8), (0 & 0xFF), (router_id >> 24),
                             ((router_id >> 16) & 0x00FF), ((router_id & 0xFFFF) >> 8), (router_id & 0xFF),
                             (0 >> 24), ((0 >> 16) & 0x00FF), ((0 & 0xFFFF) >> 8), (0 & 0xFF),
                             (0 >> 24), ((0 >> 16) & 0x00FF), ((0 & 0xFFFF) >> 8), (0 & 0xFF),
                             (metric >> 24), ((metric >> 16) & 0x00FF), ((metric & 0xFFFF) >> 8), (metric & 0xFF)])
    return entryPacket


# This creates the packet to be sent
def create_packet(router_id, command, entries):
    version = 2
    packet = bytearray([command, version, (router_id >> 8), (router_id & 0xFF)])
    if command == 2:
        packet.extend(entries)
    return packet


def packet_check(packet):
    version = 2
    if packet[0] != 2 or packet[0] != 1:
        return False
    if packet[1] != version:
        return False
    if (packet[2] << 8 | packet[3]) :
        return False


class RIPProtocol:
    def __init__(self, router_info):

        self.router_info = router_info
        print(self.router_info._router_id)
        # 1
        self._routing_table = {}

        self._routing_table[router_info._router_id] = router_info
        # print(self._routing_table)
        self.route = []
        self.route.append(self.router_info)

        print("done1",self.route)
        # self.init_routing_table()
        print("done2")
        self.print_routing_table()
        print("done")

    # def init_routing_table(self):
    #     for router_id, router_data in self.router_info.items():
    #         outputs = router_data['outputs']
    #         for output_port, metric, dest_router_id in outputs:
    #             route = Router(dest_router_id, [], [])  # Initialize router objects
    #             self._routing_table[output_port] = route

    def print_routing_table(self):
            print(f"Router ID: {self.router_info.get_router_id()}")

            # Debugging print statements
            next_hop = self.router_info.get_next_hop()
            print("Next Hop:", next_hop)
            
            metric = self.router_info.get_metric()
            print("Metric:", metric)
            
            deletion_timer = self.router_info.get_deletion_timer()
            print("Deletion Timer:", deletion_timer)
            
            garbage_timer = self.router_info.get_garbage_timer()
            print("Garbage Timer:", garbage_timer)
            
            state = self.router_info.get_state()
            print("State:", state)

            table = [
                f"+----------------+----------------+----{self.router_info.get_router_id()}------------+----------------+----------------+",
                "+----------------+----------------+----------------+----------------+----------------+",
                "| Destination    | Next Hop       | Metric         | Deletion Timer | Garbage Timer  | State          |",
                "+----------------+----------------+----------------+----------------+----------------+"
            ]

            # Handle the case where garbage_timer is None
            if garbage_timer is None:
                garbage_timer_str = "N/A"
            else:
                garbage_timer_str = str(garbage_timer)

            # Append data to the table
            table.append("| {0:<14} | {1:<14} | {2:<14} | {3:<14} | {4:<14} | {5:<14} |".format(
                "destination_value", next_hop, metric, deletion_timer, garbage_timer_str, state))

            table.append("+----------------+----------------+----------------+----------------+----------------+")

            for row in table:
                print(row)



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
