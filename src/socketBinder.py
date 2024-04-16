import socket
import select

LOCAL_HOST = "127.0.0.1"


class RouterInterface:

    def __init__(self, input_ports):
        print("socket class:", input_ports)
        # 6000, 6001, 6002
        self.sockets = {}
        self._time_out = 1
        self._input_ports = input_ports
        self.single_port = input_ports[0]
        print(f"this is input ports: {self.single_port}", type(self.single_port))
        self.init_sockets()
        print("donee")

    def init_sockets(self):
        try:
            for port in self._input_ports:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.bind((LOCAL_HOST, port))
                self.sockets[port] = sock
                print(f"Socket for port {self.sockets[port]} initialised")
        except socket.error as error:
            print("Error: Failed to create socket", error)

    def get_sockets(self):
        return self.sockets

    def get_num_sockets(self):
        return len(self.sockets)

    def get_num_ports(self):
        return len(self._input_ports)

    def receive(self):
        """
        Returns:
            data (list): List of received data from sockets
        """
        try:
            sockets = list(self.sockets.values())
            # print(f"################list of sockets:{sockets}################")
            readable_sockets, _, _ = select.select(sockets, [], [], self._time_out)
            data = []
            for socket in readable_sockets:
                data.append(socket.recv(1024))
            return data
        except socket.error as error:
            print("Error: Failed to receive data", error)
            return []

    def send(self, data, port):
        """
        Paramaters: data (bytes): Data to send, Port (int): Port to send data to
        """
        try:
            # ??
            if not isinstance(data, bytearray):
                raise ValueError(f"Expected data to be bytes, but got {type(data)}")
            print(f"sockets:{self.sockets[self.single_port]}")
            sending_socket = self.sockets[self.single_port]
            dest = (LOCAL_HOST, port)
            sending_socket.sendto(data, dest)
        except KeyError:
            print(f"The port:{port} for sending packet does not exist")
        except socket.error as error:
            print("Error: Unable to send data with the socket\n" + error)

    def __str__(self):
        sockets_info = ""
        for port, sock in self.sockets.items():
            sockets_info += f"Port {port}: {sock.getsockname()}, "
        sockets_info = sockets_info.rstrip(", ")
        return f"Host: {LOCAL_HOST}, Input Ports: {self._input_ports}, Sockets Info: {sockets_info}, Num Sockets: {self.get_num_sockets()}, Num Ports: {self.get_num_ports()}"
