import os
from Route import *

class RoutingTable:
    def __init__(self):
        self.routes = []
        self.router_id = None

    def print_table(self):
        
        table = [
            "                                           Router Id: {}                              ".format(self.router_id),
            "+-----------------+-----------------+-----------------+-----------------+-----------------+-----------------+",
            "| Destination     | Next Hop        | Metric          | Deletion Timer  | Garbage Timer   | State           |",
            "+-----------------+-----------------+-----------------+-----------------+-----------------+-----------------+"
        ]

        for route in self.routes:
            if route.get_garbage_timer() > 2:
                state = "Unreachable"
            else:
                state = "Active"
            table.append("| {0:<15} | {1:<15} | {2:<15} | {3:<15} | {4:<15} | {5:<15} |".format(route.destination, route.next_hop, route.metric, route.get_deletion_timer(), route.get_garbage_timer(), state))
        table.append("+-----------------+-----------------+-----------------+-----------------+-----------------+-----------------+")
        if os.name == 'nt':  # Windows
            os.system('cls')
        else:  # Linux or macOS
            os.system('clear')
        print("\n".join(table))
    
    def set_router_id(self, router_id):
        self.router_id = router_id

    def is_route_known(self, router_id):
        
        return router_id in [route.destination for route in self.routes]

    def add_route(self, destination, next_hop, metric):
      
        self.routes.append(Route(destination, next_hop, metric))
        self.routes = sorted(self.routes, key=lambda x: x.destination)
    
    def get_route_id_by_id(self, router_id):
      
        for route in self.routes:
            if route.destination == router_id:
                return route

    def check_route_timers(self):
     
        state = False
        routes_to_remove = set()

        for route in self.routes:
            timer_check_result = route.check_timers()

            if timer_check_result == 0: 
                routes_to_remove.add(route)
                routes_to_remove.update([x for x in self.routes if x.next_hop == route.destination])
            elif timer_check_result in [0, 1]:
                state = True

        if routes_to_remove:
            updated_routes = []
            for route in self.routes:
                if route not in routes_to_remove:
                    updated_routes.append(route)
            self.routes = updated_routes
        return state

