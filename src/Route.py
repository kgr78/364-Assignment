import datetime
from gc import garbage
import time


class Route:
  
    def __init__(self, destination, next_hop, metric):
        self.destination = destination
        self.next_hop = next_hop
        self.metric = metric
        self.deletion_timer = datetime.datetime.now()
        self.garbage_timer = None
        self.timer_limit = 30 # from 
        self.router_id = None
    
    def set_router_id(self, router_id):
        self.router_id = router_id
    
    def get_deletion_timer(self):
    
        if self.deletion_timer:
            return (datetime.datetime.now() - self.deletion_timer).seconds
        return 0

    def get_garbage_timer(self):
       
        if self.garbage_timer:
            return (datetime.datetime.now() - self.garbage_timer).seconds
        return 0
        
    def reset_timers(self):
       
        self.deletion_timer = datetime.datetime.now()
        self.garbage_timer = None

    def mark_for_deletion(self):
        self.deletion_timer = None
        self.garbage_timer = datetime.datetime.now()
        self.metric = 16
    
    
    def check_timers(self):
       
        if self.get_garbage_timer() > self.timer_limit:
            return 0
        if self.get_deletion_timer() > self.timer_limit:
            self.mark_for_deletion()
            return 1
        return 2

    def update_route(self, destination, next_hop, metric):
    
        self.destination = destination
        self.next_hop = next_hop
        self.metric = metric
        self.reset_timers()
        
