import logging
from thunderpush.messenger import Messenger

logger = logging.getLogger()


class SortingStation(object):
    """ Handles dispatching messages to Messengers. """

    _instance = None

    def __init__(self):
        self.messengers_by_apikey = {}

    @classmethod
    def instance(cls):
        if cls._instance:
            return cls._instance
        self = cls._instance = cls()
        return self

    def destroy(self):
        for messanger in self.messangers_by_apikey.values():
            messanger.destroy()
        SortingStation._instance = None

    def create_messenger(self, apikey, apisecret):
        messenger = Messenger(apikey, apisecret)
        self.messengers_by_apikey[apikey] = messenger
        return messenger

    def delete_messenger(self, messenger):
        messenger.destroy()
        del self.messengers_by_apikey[messenger.apikey]

    def get_messenger_by_apikey(self, apikey):
        return self.messengers_by_apikey.get(apikey, None)
