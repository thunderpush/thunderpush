import logging
import tornado.web
from thunderpush.sortingstation import SortingStation

logger = logging.getLogger()

try:
    import simplejson as json
except ImportError:
    import json


def is_authenticated(f):
    """ Decorator used to check if a valid api key has been provided. """

    def run_check(self, *args, **kwargs):
        ss = SortingStation.instance()

        apisecret = self.request.headers.get('X-Thunder-Secret-Key', None)
        messenger = ss.get_messenger_by_apikey(kwargs['apikey'])

        if not messenger or apisecret != messenger.apisecret:
            self.error("Wrong API key/secret.", 401)
            return

        # pass messenger instance to handler
        kwargs['messenger'] = messenger

        f(self, *args, **kwargs)

    return run_check


def is_json(f):
    """ Used to check if the body of the request is valid JSON. """

    def run_check(self, *args, **kwargs):
        try:
            json.loads(self.request.body)
            f(self, *args, **kwargs)
        except ValueError:
            self.error("Request body is not valid JSON.", 400)
            return

    return run_check


class ThunderApiHandler(tornado.web.RequestHandler):
    def response(self, data, code=200):
        if code != 200:
            # if something went wrong, we include returned HTTP code in the
            # JSON response
            data["status"] = code

        self.write(json.dumps(data) + "\n")
        self.set_status(code)

    def error(self, message, code=500):
        self.response({"message": message}, code)

    def prepare(self, *args, **kwargs):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "X-Thunder-Secret-Key")
        self.set_header("Access-Control-Allow-Methods", "GET, POST, DELETE")

    def options(self, *args, **kwargs):
        pass


class ChannelHandler(ThunderApiHandler):
    @is_authenticated
    @is_json
    def post(self, *args, **kwargs):
        """ Sends messages to a channel. """

        messenger = kwargs['messenger']
        channel = kwargs['channel']

        count = messenger.send_to_channel(channel, self.request.body)
        self.response({"count": count})

        logger.debug("Message has been sent to %d users." % count)

    @is_authenticated
    def get(self, *args, **kwargs):
        """ Retrieves the number of users online. """

        messenger = kwargs['messenger']
        channel = kwargs['channel']

        users = \
            [user.userid for user in messenger.get_users_in_channel(channel)]

        self.response({"users": users})

class EventHandler(ThunderApiHandler):
    @is_authenticated
    @is_json
    def post(self, *args, **kwargs):
        """ Sends messages to a channel. """

        messenger = kwargs['messenger']
        event = kwargs['event']

        try:
            content_parsed = json.loads(self.request.body)
            content_channels = content_parsed.get('channels')
            del content_parsed['channels']
            count = 0
            if type(content_channels) is list:
                for channel in content_channels:
                    count += messenger.send_to_channel(channel, json.dumps(content_parsed), event)
            else:
                count += messenger.send_to_channel(content_channels, json.dumps(content_parsed), event)
            self.response({"count": count})

            logger.debug("Message has been sent to %d users." % count)
        except KeyError:
            self.error("Request has no channels.", 400)
            return


class UserCountHandler(ThunderApiHandler):
    """ Retrieves the number of users online. """

    @is_authenticated
    def get(self, *args, **kwargs):
        messenger = kwargs['messenger']

        self.response({"count": messenger.get_user_count()})


class UserHandler(ThunderApiHandler):
    @is_authenticated
    def get(self, *args, **kwargs):
        """ Retrieves the number of users online. """

        messenger = kwargs['messenger']
        user = kwargs['user']

        is_online = messenger.is_user_online(user)
        self.response({"online": is_online}, 200)

    @is_authenticated
    @is_json
    def post(self, *args, **kwargs):
        """ Sends a message to a user. """

        messenger = kwargs['messenger']
        user = kwargs['user']

        count = messenger.send_to_user(user, self.request.body)
        self.response({"count": count})

        logger.debug("Message has been sent to %d users." % count)

    @is_authenticated
    def delete(self, *args, **kwargs):
        """ Forces logout of a user. """

        messenger = kwargs['messenger']
        user = kwargs['user']

        messenger.force_disconnect_user(user)

        # no response
        self.set_status(204)
