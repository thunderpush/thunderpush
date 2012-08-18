import time
import logging
import json
import tornado.ioloop
import tornado.web
from tornado import websocket, web
from tornado.ioloop import IOLoop
from sockjs.tornado import SockJSRouter, SockJSConnection

try:
    import json
except ImportError:
    import simplejson as json 

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

class Messenger(object):
    """ 
    Handles dispatching messages to Channels and Users
    for given client.
    """
    
    def __init__(self, apikey, apisecret, *args, **kwargs):
        self.apikey = apikey
        self.apisecret = apisecret
        self.users = {}
        self.channels = {}
        self.user_count = 0

    def send_to_channel(self, channel, message):
        """ 
        Sends a message to given channel
        Returns a count of messages sent
        """

        try:
            channel = self.channels[channel]
        except KeyError:
            return 0

        count = 0

        for user in channel:
            user.send(message)
            count += 1

        return count

    def send_to_user(self, user, message):
        pass

    def subsribe_user(self, user):
        self.user_count += 1

    def subsribe_user_to_channel(self, user, channel):
        logger.debug("%s subscribed to %s." % (user.userid, channel,))

        self.channels.setdefault(channel, []).append(user)

        logger.debug("User count in %s: %d." % (channel, self.get_channel_user_count(channel)))

    def unsubscribe_user(self, user):
        for name in self.channels.iterkeys():
            try:
                self.channels[name].remove(user)
            except (KeyError, ValueError):
                pass

        self.user_count -= 1

    def get_user_count(self):
        return self.user_count

    def get_channel_user_count(self, channel):
        channel = self.channels.get(channel, None)

        if channel:
            return len(channel)
        else:
            logger.debug("Channel %s not found." % (channel,))
            return 0

class SortingStation(object):
    """ Handles dispatching messages to Messengers. """

    def __init__(self, *args, **kwargs):
        self.messengers_by_apikey = {}
        self.messengers_by_apisecret = {}

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

class ChannelMessageHandler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        messenger = ss.get_messenger_by_apisecret(kwargs['apisecret'])

        if messenger:
            count = messenger.send_to_channel(kwargs['channel'], self.request.body)

            logger.debug("Message has been sent to %d users." % count)

            self.write(json.dumps({"status": "ok", "count": count}) + "\n")
        else:
            self.write(json.dumps({"status": "error", "message": "Wrong API secret."}) + "\n")

class UserCountHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        messenger = ss.get_messenger_by_apisecret(kwargs['apisecret'])

        if messenger:
            user_count = messenger.get_user_count()

            self.write(json.dumps({"status": "ok", "count": user_count}) + "\n")
        else:
            self.write(json.dumps({"status": "error", "message": "Wrong API secret."}) + "\n")

class ThunderSocketHandler(SockJSConnection):
    def on_open(self, info):
        logger.debug("New connection opened.")
        self.connected = False

    def on_message(self, msg):
        logger.debug("Got message: %s" % msg)

        self.process_message(msg)

    def on_close(self):
        messenger = ss.get_messenger_by_apikey(self.apikey)

        if messenger:
            messenger.unsubscribe_user(self)

        logger.debug("User %s has disconnected." % self.userid)

    def process_message(self, msg):
        tokens = msg.split(" ")

        if tokens[0] == "CONNECT":
            if self.connected:
                logger.warning("User already connected.")
                return

            try:
                self.userid, self.apikey = tokens[1].split(":")
            except ValueError:
                logger.warning("Invalid message syntax.")

            messenger = ss.get_messenger_by_apikey(self.apikey)

            if messenger:
                messenger.subsribe_user(self)
                self.connected = True
            else:
                logger.warning("Invalid API key.")

                # inform client that the key was not good
                self.send("WRONGKEY")
                self.close()
        elif tokens[0] == "SUBSCRIBE":
            if not self.connected:
                logger.warning("User not connected.")
                return

            channels = tokens[1].split(":")
            messenger = ss.get_messenger_by_apikey(self.apikey)
                
            for channel in channels:
                messenger.subsribe_user_to_channel(self, channel)
        else:
            logger.warning("Received uncregonizable message: %s." % msg)

ThunderRouter = SockJSRouter(ThunderSocketHandler, "/connect")

application = tornado.web.Application([
    (r"/1\.0\.0/(?P<apisecret>.+)/users/", UserCountHandler),
    (r"/1\.0\.0/(?P<apisecret>.+)/channels/(?P<channel>.+)/", ChannelMessageHandler),
] + ThunderRouter.urls, debug=True)

if __name__ == "__main__":
    ss = SortingStation()
    ss.create_messenger("key", "secretkey")

    application.listen(8080)
    tornado.ioloop.IOLoop.instance().start()
    