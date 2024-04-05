import socket
import select

LOCAL_HOST = "127.0.0.1"


class RouterInterface:

    def __init__(self, input_ports):
        self._input_ports = input_ports
        self._sockets = {}
        self._time_out = 1
        self._port = input_ports[0]
        self.init_sockets()

    def init_sockets(self):
        try:
            for port in self._input_ports:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.bind((LOCAL_HOST, port))
                self._sockets[port] = sock
        except socket.error as error:
            print("Error: Failed to create socket", error)

    def get_sockets(self):
        return self._sockets

    def get_num_sockets(self):
        return len(self._sockets)

    def get_num_ports(self):
        return len(self._input_ports)

    def receive(self):
        """
        Returns:
            data (list): List of received data from sockets
        """
        try:
            sockets = list(self._sockets.values())
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
            if not isinstance(data, bytes):
                raise ValueError(f"Expected data to be bytes, but got {type(data)}")
            sending_socket = self._sockets[self._port]
            dest = (LOCAL_HOST, port)
            sending_socket.sendto(data, dest)
        except KeyError:
            print(f"The port:{port} for sending packet does not exist")
        except socket.error as error:
            print("Error: Unable to send data with the socket\n" + error)
    def __str__(self):
        sockets_info = ""
        for port, sock in self._sockets.items():
            sockets_info += f"Port {port}: {sock.getsockname()}, "
        sockets_info = sockets_info.rstrip(", ")
        return f"Host: {LOCAL_HOST}, Input Ports: {self._input_ports}, Sockets Info: {sockets_info}, Num Sockets: {self.get_num_sockets()}, Num Ports: {self.get_num_ports()}"
