import socket
import select
import random
import time

from ripRoute import Router


def packet_check(packet):
    version = 2
    if packet[0] != 2 and packet[0] != 1:
        return False
    if packet[1] != version:
        return False
    # This needs to be changed around so that it can check the id of the router
    # if (packet[2] << 8 | packet[3]) != 0:
    # if packet[0] == 2:


TIMER_INTERVAL = 30


class RIPProtocol:
    def __init__(self, router_info):
        self.router_info = router_info
        print(self.router_info._router_id)
        # 1
        self._routing_table = {}
        self._routing_table[router_info._router_id] = router_info
        for router_id, router_obj in self._routing_table.items():
            print(f"Router ID: {router_id}")
            print(f"Router Object: {router_obj}")
        print(self._routing_table)

        self.route = []
        self.route.append(self.router_info)
        self.timer_interval = TIMER_INTERVAL
        self.timer_start = time.time()
        print("done1", self.route)
        # self.init_routing_table()
        print("done2")
        self.print_routing_table()
        print("done")

        #2
        # send the routing table to the neighbors
        self.send_packets()
    def send_packets(self):
        for port in self.router_info.get_inputs():
            print("sending on port", port)
    
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
             "+----------------+----------------+----------------+----------------+----------------+----------------+",
             "| Destination    | Next Hop       | Metric         | Deletion Timer | Garbage Timer  | State          |",
             "+----------------+----------------+----------------+----------------+----------------+----------------"
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

    def create_entry_packet(self, router_id, metric):
        address_family = 2
        entryPacket = bytearray([(address_family >> 8), (address_family & 0xFF), (0 >> 8), (0 & 0xFF), (router_id >> 24),
                                 ((router_id >> 16) & 0x00FF), ((router_id & 0xFFFF) >> 8), (router_id & 0xFF),
                                 (0 >> 24), ((0 >> 16) & 0x00FF), ((0 & 0xFFFF) >> 8), (0 & 0xFF),
                                 (0 >> 24), ((0 >> 16) & 0x00FF), ((0 & 0xFFFF) >> 8), (0 & 0xFF),
                                 (metric >> 24), ((metric >> 16) & 0x00FF), ((metric & 0xFFFF) >> 8), (metric & 0xFF)])
        return entryPacket

# This creates the packet to be sent
    def create_packet(self, router_id, command, entries):
        version = 2
        packet = bytearray([command, version, (router_id >> 8), (router_id & 0xFF)])
        if command == 2:
            packet.extend(entries)
        return packet

    def init_routing_table(self):
        for router_id, router_data in self.router_info.items():
            outputs = router_data['outputs']
            for output_port, metric, dest_router_id in outputs:
                self._routing_table[output_port] = {
                    'next': dest_router_id,
                    'timeout': None,
                    'state': 'active'
                }

    def update_routing_table(self, packet):
        command = packet[0]
        version = packet[1]
        router_id = (packet[2] << 8) | packet[3]

        if command == 2 and version == 2:
            entries = packet[4:]
            for i in range(0, len(entries), 20):
                dest_router_id = (entries[i] << 24) | (entries[i + 1] << 16) | (entries[i + 2] << 8) | entries[i + 3]
                metric = (entries[i + 16] << 24) | (entries[i + 17] << 16) | (entries[i + 18] << 8) | entries[i + 19]

                # Check if the destination router ID already exists in the routing table
                if dest_router_id in self._routing_table:
                    existing_entry = self._routing_table[dest_router_id]
                    existing_metric = existing_entry['metric']

                    # Handle metric 16 (route not usable)
                    if metric == 16:
                        if existing_metric != 16:
                            # Mark the route as invalid if it wasn't already
                            existing_entry['metric'] = 16
                            existing_entry['state'] = 'invalid'
                            print(f"Route to {dest_router_id} marked as invalid due to metric 16.")
                    else:
                        # Update the routing table only if the new metric is better (lower) or if it's invalid (16)
                        if metric < existing_metric or existing_metric == 16:
                            existing_entry['next_hop'] = router_id
                            existing_entry['metric'] = min(metric, 15)  # Cap the metric at 15
                            existing_entry['state'] = 'active'
                            print(f"Route to {dest_router_id} updated with metric {metric} via {router_id}.")
                else:
                    # Add a new entry to the routing table for the destination router
                    self._routing_table[dest_router_id] = {
                        'next_hop': router_id,
                        'metric': min(metric, 15),
                        'state': 'active'
                    }
                    print(f"Added new route to {dest_router_id} with metric {metric} via {router_id}.")

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

    def format_routing_entries(self):
        entries = []
        for dest_router_id, route_data in self._routing_table.items():
            entry_data = self.create_entry_packet(dest_router_id, route_data['metric'])
            entries.extend(entry_data)
        return entries

    def process_packet(self, packet):
        command = packet[0]
        version = packet[1]
        if packet_check(packet) is False:
            print("Packet failed the packet check")
            return
        else:
            if command == 1:
                # Process triggered updates or responses
                self.update_routing_table(packet)
            elif command == 2:
                # Process periodic updates
                self.update_routing_table(packet)

    def handle_timers(self):
        pass

    def send_data(self, output_port, data):
        pass

    # def generate_periodic_update(self):
    #     entries = self.format_routing_entries()
    #     return self.create_packet(2, entries)

    # def send_periodic_updates(self):
    #     while True:
    #         if time.time() - self.timer_start >= self.timer_interval:
    #             periodic_update_packet = self.generate_periodic_update()
    #             self.send_to_neighbors(periodic_update_packet)
    #             self.timer_interval = random.uniform(0.8 * TIMER_INTERVAL, 1.2 * TIMER_INTERVAL)
    #             self.timer_start = time.time()
