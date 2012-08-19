import logging
import tornado.web
from thunderpush.sortingstation import SortingStation

logger = logging.getLogger()

try:
    import json
except ImportError:
    import simplejson as json 

def is_authenticated(f):
    """ Decorator used to check if a valid api key has been provided. """

    def run_check(self, *args, **kwargs):
        try:
            apisecret = self.request.headers['X-Thunder-Secret-Key']
        except KeyError:
            self.response({
                "status": "error", "message": "Missing apisecret header."
            }, 400)

            return

        ss = SortingStation.instance()
        messenger = ss.get_messenger_by_apikey(kwargs['apikey'])

        if not messenger or messenger.apisecret != apisecret:  
            self.response({
                "status": "error", "message": "Wrong API key/secret."
            }, 401)

            return

        # pass messenger instance to handler
        kwargs['messenger'] = messenger

        f(self, *args, **kwargs)
    return run_check

class ThunderApiHandler(tornado.web.RequestHandler):
    def response(self, data, code=200):
        self.write(json.dumps(data) + "\n")
        self.set_status(code)

class ChannelHandler(ThunderApiHandler):
    @is_authenticated
    def post(self, *args, **kwargs):
        """ Sends messages to specified channel. """

        messenger = kwargs['messenger']
        channel = kwargs['channel']

        count = messenger.send_to_channel(channel, self.request.body)
        self.response({"status": "ok", "count": count})

        logger.debug("Message has been sent to %d users." % count)

    @is_authenticated
    def get(self, *args, **kwargs):
        """ Retrieves the number of users online. """

        messenger = kwargs['messenger']
        channel = kwargs['channel']
        
        users = [user.userid for user in messenger.get_users_in_channel(channel)]

        self.response({"status": "ok", "users": users})

class UserCountHandler(ThunderApiHandler):
    """ Retrieves the number of users online. """

    @is_authenticated
    def get(self, *args, **kwargs):
        messenger = kwargs['messenger']

        self.response({"status": "ok", "count": messenger.get_user_count()})

class UserOnlineHandler(ThunderApiHandler):
    """ Retrieves the number of users online. """

    @is_authenticated
    def get(self, *args, **kwargs):
        messenger = kwargs['messenger']
        user = kwargs['user']
        
        is_online = messenger.is_user_online(user)

        self.response({
            "status": "ok", "online": is_online
        }, [404, 200][int(is_online)])
