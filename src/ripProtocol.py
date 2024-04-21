import random
import select
import socket
import sys
import datetime
from time import sleep

from RoutingTable import *
from ConfigParser import *

LOCAL_HOST = "127.0.0.1"
class ErrorHandler:
    """
    ErrorHandler class logs error and prints error messages if any error occurs. Note: must set the print_logs flag to True.
    """
    def __init__(self, print_logs):
        self.print_logs = print_logs

    def log(self, message):
        if self.print_logs:
            print(message)
class RipRouter:
    """
    The RipRouter class represents a router implementing the RIP (Routing Information Protocol) protocol v2. 
    It handles the initialization of the router with configuration data, sending and receiving RIP packets, 
    updating the routing table based on received packets, and managing periodic updates and route timers.
    """
    def __init__(self, config_filename):
        """
        Initializes the RipRouter object with the given configuration file.
        Parameters:
            config_filename (str): The name of the configuration file.
        """
        self.error_handler = ErrorHandler(print_logs=False)
        config_parser = ConfigParser()
        self.router = config_parser.read_config_file(config_filename)
        self.router_id = self.router.get_router_id()
        self.input_ports = self.router.get_input_ports()
        self.output_ports = self.router.get_outputs()
        self.input_sockets = self.setup_input_sockets()
        self.routing_table = RoutingTable()
        self.routing_table.set_router_id(self.router_id)
        self.periodic_update_timer = datetime.datetime.now()
   
    def get_outputs(self):
        """
        Returns:
            output_ports (list): The list of output ports.
        """
        return self.output_ports
    def setup_input_sockets(self):
        """
        Sets up the input sockets for the RIP protocol.
        Returns:
            sockets (list): A list of input sockets.
        """
        sockets = []
        for port in self.input_ports:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.bind((LOCAL_HOST, port))
            sockets.append(sock)
        return sockets

    def create_rip_packet(self):
        """
        Creates a RIP packet from the routing table.
        Returns:
            packet (bytearray): The created RIP packet.
        """

        packet = bytearray(4)
        header_command = 0x02
        header_version = 0x02
        packet[0] = header_command
        packet[1] = header_version

        packet[2] = self.router_id >> 8
        packet[3] = (self.router_id & 0x00FF)

        for route in self.routing_table.routes:
            rip_entry = bytearray(20)

            # Check if the destination is valid
            if route.destination < 1 or route.destination > 64000:
                self.error_handler.log(f"Error: Invalid destination value, destination: {route.destination}")
            else:
                rip_entry[4] = route.destination >> 24
                rip_entry[5] = (route.destination & 0x00FF0000) >> 16
                rip_entry[6] = (route.destination & 0x0000FF00) >> 8
                rip_entry[7] = (route.destination & 0x000000FF)

            # Check if the metric is valid
            if route.metric < 1 or route.metric > 16:
                self.error_handler.log(f"Error: Invalid metric value, metric: {route.metric}")
            else:
                rip_entry[16] = route.metric >> 24
                rip_entry[17] = (route.metric & 0x00FF0000) >> 16
                rip_entry[18] = (route.metric & 0x0000FF00) >> 8
                rip_entry[19] = (route.metric & 0x000000FF)

            packet.extend(rip_entry)

        return packet

    def send_rip_packets(self):
        """
        Sends RIP packets to all the output ports.
        """
        message = self.create_rip_packet()
        send_socket = self.input_sockets[0]
        for port in self.router.get_outputs():
            try:
                send_socket.sendto(message, (LOCAL_HOST, port))
            except socket.error as e:
                self.error_handler.log(f"Error occurred while sending RIP packet to port {port}: {e}")
    def close_input_sockets(self):
        """
        Closes all the input sockets. Used for testing, else it will cause an resource allocation error.
        """
        for socket in self.input_sockets:
            socket.close()
        self.input_sockets.clear()

    def receive_packets(self):
        """
        Receives RIP packets from all the input ports.
        """
        timeout = 1
        readable_sockets, _, _ = select.select(self.input_sockets, [], [], timeout)

        for socket in readable_sockets:
            data, _ = socket.recvfrom(1024)
            self.process_received_packet(data)

    def process_received_packet(self, data):
        """
        Processes a received RIP packet and updates the routing table if necessary. If updated than sends a new RIP packet.
        Parameters:
            data (bytearray): The received RIP packet.

        """
        routing_table_updated = False

        rip_header = data[:4]
        rip_data = data[4:]
        command = rip_header[0]
        version = rip_header[1]
        next_hop_router_id = int.from_bytes(rip_header[2:], "big")

        if command != 2:
            self.error_handler.log(f"Error: Command is invalid, command:{command}")
            return
        if version != 2:
            self.error_handler.log(f"Error: Version is invalid, version:{version}")
            return
        if not (0 < next_hop_router_id < 64001):
            self.error_handler.log(f"Error: Router id is invalid, router id:{next_hop_router_id}")
            return
        if not self.router.is_router_in_outputs(next_hop_router_id):
            self.error_handler.log(f"Dropping packet: Router id not in outputs, router id:{next_hop_router_id}")
            return

        output = self.router.get_output_by_router_id(next_hop_router_id)
        if not self.routing_table.is_route_known(next_hop_router_id):
            self.routing_table.add_route(next_hop_router_id, next_hop_router_id, output["metric"])
            self.error_handler.log("is_route_known == False")
            routing_table_updated = True
        else:
            route = self.routing_table.get_route_id_by_id(next_hop_router_id)
            if output["metric"] < route.metric:
                route.update_route(next_hop_router_id, next_hop_router_id, output["metric"])
                routing_table_updated = True
            if route.next_hop == next_hop_router_id:
                route.reset_timers()

        routes = []

        for i in range(0, int(len(rip_data)), 20):
            routes.append(rip_data[i:i + 20])

        for route in routes:
            afi = int.from_bytes(route[:2], 'big')
            if afi != 0:
                self.error_handler.log(f"Error: afi is invalid, afi:{afi}")
            else:
                router_id = int.from_bytes(route[4:8], 'big')
                self.error_handler.log(f"Route router id: {router_id}")
                if 0 < router_id < 64001:
                    if router_id != self.router_id:
                        output = self.router.get_output_by_router_id(next_hop_router_id)
                        metric = int.from_bytes(route[16:], 'big')
                        route_object = self.routing_table.get_route_id_by_id(router_id)

                        if (0 < (metric + output["metric"]) < 17) or metric == 16:
                            if route_object:
                                if route_object.next_hop == next_hop_router_id:
                                    if metric == 16:
                                        if route_object.garbage_timer is None:
                                            route_object.mark_for_deletion()
                                            routing_table_updated = True
                                    elif route_object.metric != metric + output["metric"]:
                                        routing_table_updated = True
                                    else:
                                        route_object.reset_timers()
                                elif metric + output["metric"] < route_object.metric:
                                    route_object.update_route(route_object.destination, next_hop_router_id,
                                                            metric + output["metric"])
                                    routing_table_updated = True
                            elif metric < 16:
                                self.routing_table.add_route(router_id, next_hop_router_id,
                                                            metric + output["metric"])
                                routing_table_updated = True
                        else:
                            self.error_handler.log(f"Error: metric out of bound, metric:{metric}")

        if routing_table_updated:
            self.send_rip_packets()

    
    def get_update_timer_duration(self):
        """
        Calculates the duration since the last periodic update
        """
        return (datetime.datetime.now() - self.periodic_update_timer).seconds
    
    def reset_periodic_update_timer(self):
        """
        Resets the periodic update timer
        """
        self.periodic_update_timer = datetime.datetime.now()

    def check_timeout_entries_periodically(self):
        """
        Periodically checks for timeout entries in the routing table and sends RIP packets if needed.
        The 30-second timer is offset by a small random time (+/- 0 to 5 seconds) each time it is set. 
        (Implementors may wish to consider even larger variation in the light of recent research results [10])
        """
        random_offset_period = 11 + random.randrange(-5, 5)
        if self.get_update_timer_duration() > random_offset_period:

            self.send_rip_packets()
            self.reset_periodic_update_timer()
    
    def check_route_timers(self):
        """
        Checks for timeout entries in the routing table and sends RIP packets if needed.
        """
        if self.routing_table.check_route_timers():
            self.send_rip_packets()

    def rip_protocol(self):
        """
        The main RIP protocol loop.
        """
        
        self.send_rip_packets()
      
        while(1):
            self.routing_table.print_table()
            self.receive_packets()
            self.check_timeout_entries_periodically()
            self.check_route_timers()
            sleep(1)

def main(config_filename):
    try:
        router = RipRouter(config_filename)
        router.rip_protocol()
    except Exception as exception:
            print(exception)

if __name__=="__main__":
    if len(sys.argv) != 2:
        print("Error: Invalid number of arguments, usage: python3 RipProtocol.py <config_filename>")
    else:
        config_filename = sys.argv[1]
        main(config_filename)
