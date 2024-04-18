import datetime

class Router:
    """Object that represents RIP v2 route"""
    def __init__(self, router_id, inputs , outputs, next_hop, metric, state):
        self._router_id = router_id
        self._inputs = inputs
        self._outputs = outputs
        self._deletion_timer = datetime.datetime.now()
        self._garbage_timer = None
        self._timer_limit = 30
        self._state = 'active'

        self.next_hop = next_hop
        self.metric = metric
        self.state = state

    def get_router_id(self):
        return self._router_id

    def get_inputs(self):
        return self._inputs

    def get_outputs(self):
        return self._outputs

    def start_garbage_timer(self):
        self._garbage_timer = datetime.datetime.now()

    # def reset_garbage_timer(self):
    #     self._garbage_timer = None

    # def is_expired(self):
    #     if self._garbage_timer is None:
    #         return False
    #     else:
    #         time_diff = datetime.datetime.now() - self._garbage_timer
    #         return time_diff.total_seconds() > self._timer_limit

    # def set_state(self, state):
    #     self._state = state

    # def get_state(self):
    #     return self._state
