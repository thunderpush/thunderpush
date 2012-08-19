import logging

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

    def send_to_channel(self, channel, message):
        """ 
        Sends a message to given channel
        Returns a count of messages sent
        """

        users = self.get_users_in_channel(channel)
        count = len(users)

        for user in users:
            user.send(message)

        return count

    def send_to_user(self, user, message):
        pass

    def subsribe_user(self, user):
        self.user_count += 1

        if user in self.users:
            self.users[user.userid] += 1
        else:
            self.users[user.userid] = 1

    def subsribe_user_to_channel(self, user, channel):
        self.channels.setdefault(channel, []).append(user)

        logger.debug("%s subscribed to %s." % (user.userid, channel,))
        logger.debug("User count in %s: %d." % 
            (channel, self.get_channel_user_count(channel)))

    def unsubscribe_user(self, user):
        for name in self.channels.iterkeys():
            try:
                self.channels[name].remove(user)
            except (KeyError, ValueError):
                pass

        self.user_count -= 1
        self.users[user.userid] -= 1

    def get_user_count(self):
        return self.user_count

    def is_user_online(self, userid):
        return bool(self.users.get(userid, 0))

    def get_channel_user_count(self, channel):
        return len(self.get_users_in_channel(channel))

    def get_users_in_channel(self, channel):
        return self.channels.get(channel, [])