import sys
sys.path.append("/Users/isma/Desktop/COSC364/RIPAssignment/364-Assignment")
from src.socketBinder import RouterInterface
import socket
import select

def test_init_sockets():

    input_ports = [5009, 5001, 5002]
    router_interface = RouterInterface(input_ports)
    assert len(router_interface.get_sockets()) == len(input_ports)

    for port in input_ports:
        assert port in router_interface.get_sockets()

def test_init_sockets_error():

    try:
        input_ports = [5000, 5001, "invalid_port"]
        router_interface = RouterInterface(input_ports)
    except TypeError as error:
        assert isinstance(error, TypeError)
    else:
        assert False

def test_receive():

    input_ports = [5000, 5001, 5002]
    router_interface = RouterInterface(input_ports)
    sender_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sender_socket.sendto(b"Test data", ("127.0.0.1", 5000))
    received_data = router_interface.receive()
    assert len(received_data) == 1
    assert received_data[0] == b"Test data"

def test_send():
 
    input_ports = [5000, 5001, 5002]
    router_interface = RouterInterface(input_ports)
    assert router_interface._input_ports == input_ports
    sender = router_interface
    receiver = RouterInterface([5013,5014,5015])
    sender.send(b'test data', 5013)
    assert receiver.receive()[0] == b"test data"
    sender.send(b'test data', 5014)
    assert receiver.receive()[0] == b"test data"

def test_str():

    input_ports = [5000, 5001, 5002]
    router_interface = RouterInterface(input_ports)
    expected_str = f"Host: 127.0.0.1, Input Ports: {input_ports}, Sockets Info: Port 5000: ('127.0.0.1', 5000), Port 5001: ('127.0.0.1', 5001), Port 5002: ('127.0.0.1', 5002), Num Sockets: {len(input_ports)}, Num Ports: {len(input_ports)}"
    assert str(router_interface) == expected_str

if __name__ == "__main__":
    print("Testing RouterInterface")
    test_init_sockets()
    test_init_sockets_error()
    test_receive()
    test_send()
    test_str()
    print("All tests passed")
