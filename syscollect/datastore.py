import os
import time

class datastore:
    def __init__(self, ttl):
        self.data = {}
        self.ttl = ttl

    def push(self, key, value):
        now = int(time.time())
        if key in self.data:
            # Kick out old junk thats older than the TTL
            while (self.data[key][0][0] + self.ttl) < now:
                del self.data[key][0]

            self.data[key] += [(now, value)]
        else:
            self.data[key] = [(now, value)]
