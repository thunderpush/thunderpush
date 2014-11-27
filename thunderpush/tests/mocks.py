class DummyThunderSocketHandler(object):
    dummyid = 1

    def __init__(self, *args, **kwargs):
        self.userid = "dummy_%d" % DummyThunderSocketHandler.dummyid
        self.connected = True

        DummyThunderSocketHandler.dummyid += 1

    def send(self, message):
        pass

    def broadcast(self, users, message):
        pass

    def force_disconnect(self):
        self.connected = False
