import datetime


class Route:
    """Object that represents RIP v2 route"""
    def __intit__(self, destination , next_hop, metric):
        self._destination = destination
        self._next_hop = next_hop
        self._metric = metric
        self._deletion_timer = datetime.datetime.now()
        self._garbage_timer = None
        self._timer_limit = 30
        self._state = 'active'

        