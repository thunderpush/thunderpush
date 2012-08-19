import logging
from thunderpush.messenger import Messenger

logger = logging.getLogger()

class SortingStation(object):
    """ Handles dispatching messages to Messengers. """

    _instance = None

    def __init__(self, *args, **kwargs):
        if self._instance:
            raise Exception("SortingStation already initialized.")

        self.messengers_by_apikey = {}
        self.messengers_by_apisecret = {}

        SortingStation._instance = self

    @staticmethod
    def instance():
        return SortingStation._instance

    def create_messenger(self, apikey, apisecret):
        messenger = Messenger(apikey, apisecret)

        self.messengers_by_apikey[apikey] = messenger
        self.messengers_by_apisecret[apisecret] = messenger

    def delete_messenger(self, messenger):
        del self.messengers_by_apikey[messenger.apikey]
        del self.messengers_by_apisecret[messenger.apisecret]

    def get_messenger_by_apikey(self, apikey):
        try:
            return self.messengers_by_apikey[apikey]
        except KeyError:
            return None

    def get_messenger_by_apisecret(self, apisecret):
        try:
            return self.messengers_by_apisecret[apisecret]
        except KeyError:
            return None

    def dispatch(self, apisecret, message, *args, **kwargs):
        """ Sends a message to specified channel or user. """

        messenger = self.get_messenger_by_apisecret(apisecret)
        
        if messenger:
            if "channel" in kwargs:
                messenger.send_to_channel(kwargs['channel'])
            elif "user" in kwargs:
                pass