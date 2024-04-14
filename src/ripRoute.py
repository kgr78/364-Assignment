import datetime

class Router:
    def __init__(self, router_id, inputs, outputs, next_hop, metric, state):
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

    def set_router_id(self, router_id):
        self._router_id = router_id

    def get_inputs(self):
        return self._inputs

    def set_inputs(self, inputs):
        self._inputs = inputs

    def get_outputs(self):
        return self._outputs

    def set_outputs(self, outputs):
        self._outputs = outputs

    def get_next_hop(self):
        return self.next_hop

    def set_next_hop(self, next_hop):
        self.next_hop = next_hop

    def get_metric(self):
        return self.metric

    def set_metric(self, metric):
        self.metric = metric

    def get_state(self):
        return self.state

    def set_state(self, state):
        self.state = state

    def get_deletion_timer(self):
        return self._deletion_timer

    def set_deletion_timer(self, deletion_timer):
        self._deletion_timer = deletion_timer

    def get_garbage_timer(self):
        return self._garbage_timer

    def set_garbage_timer(self, garbage_timer):
        self._garbage_timer = garbage_timer

    def get_timer_limit(self):
        return self._timer_limit

    def set_timer_limit(self, timer_limit):
        self._timer_limit = timer_limit
