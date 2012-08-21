import logging
import re

logger = logging.getLogger()

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

    @staticmethod
    def is_valid_channel_name(name):
        return re.match("^[a-zA-Z0-9_\-\=\@\,\.\;]{1,64}$", name) != None

    def send_to_channel(self, channel, message):
        """ 
        Sends a message to given channel.
        Returns a count of messages sent.
        """

        users = self.get_users_in_channel(channel)
        return self._send_to_users(users, message)

    def send_to_user(self, userid, message):
        """ 
        Sends a message to given user.
        Returns a count of messages sent.
        """

        users = self.users.get(userid, [])
        return self._send_to_users(users, message)

    def _send_to_users(self, users, message):
        if users:
            users[0].broadcast(users, message)

        return len(users)

    def register_user(self, user):
        self.user_count += 1
        self.users.setdefault(user.userid, []).append(user)

    def subsribe_user_to_channel(self, user, channel):
        if self.is_valid_channel_name(channel):
            self.channels.setdefault(channel, []).append(user)

            logger.debug("%s subscribed to %s." % (user.userid, channel,))
            logger.debug("User count in %s: %d." % 
                (channel, self.get_channel_user_count(channel)))
        else:
            logger.debug("Invalid channel name %s." % channel)

    def unregister_user(self, user):
        channels_to_free = []

        for name in self.channels.iterkeys():
            try:
                self.channels[name].remove(user)

                # as we can't delete keys from the dict as we are iterating
                # over it, we do it outside of this loop
                if len(self.channels[name]) == 0:
                    channels_to_free.append(name)
            except ValueError:
                pass

        # free up the memory used by empty channel index
        for channel in channels_to_free:
            del self.channels[channel]

        self.users[user.userid].remove(user)

        # free up the memory used by empty user index
        if len(self.users[user.userid]) == 0:
            del self.users[user.userid]

        self.user_count -= 1

    def get_user_count(self):
        return self.user_count

    def is_user_online(self, userid):
        return bool(self.users.get(userid, 0))

    def get_channel_user_count(self, channel):
        return len(self.get_users_in_channel(channel))

    def get_users_in_channel(self, channel):
        return self.channels.get(channel, [])
