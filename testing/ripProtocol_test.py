import socket
import multiprocessing as mp
import time

from src.main import run_checks_and_get_values
from src.ripProtocol import RIPProtocol
from src.socketBinder import RouterInterface
config_file = '../configFile/config1.txt'


def router_info():
    data = {1: {'input_ports': [6000, 6001, 6002], 'outputs': [(6003, 1, 2), (6004, 8, 7), (6005, 5, 6)]}}
    router_id = next(iter(data))
    print("Router ID:", router_id)
    for key, value in data.items():
        print("Key:", key)
        print("Value:", value)


def main():
    router_info = {}
    router_id, input_ports, outputs = run_checks_and_get_values(config_file)
    router_info[router_id] = {'input_ports': input_ports, 'outputs': outputs}
    # print("##################")
    # print(router_info)
    # # {1: {'input_ports': [6000, 6001, 6002], 'outputs': [(6003, 1, 2), (6004, 8, 7), (6005, 5, 6)]}}
    # print("##################")
    RouterInterface(input_ports)
    rip_protocol = RIPProtocol(router_info)
    input_ports = [5000, 5001, 5002]
    router_interface = RouterInterface(input_ports)
    # print(router_interface)
main()
# rounter_info()