from thunderpush.sortingstation import SortingStation
from thunderpush.handler import ThunderSocketHandler
from thunderpush import api
from thunderpush import settings

from sockjs.tornado import SockJSRouter

import tornado.ioloop
import optparse
import logging

logger = logging.getLogger()

def run_app():
    # configure logging level
    if settings.VERBOSE:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    ThunderRouter = SockJSRouter(ThunderSocketHandler, "/connect")

    # api urls
    urls = [
        (r"/1\.0\.0/(?P<apikey>.+)/users/",
            api.UserCountHandler),
        (r"/1\.0\.0/(?P<apikey>.+)/users/(?P<user>.+)/",
            api.UserHandler),
        (r"/1\.0\.0/(?P<apikey>.+)/channels/(?P<channel>.+)/", 
            api.ChannelHandler),
    ]

    # include sockjs urls
    urls += ThunderRouter.urls

    application = tornado.web.Application(urls, settings.DEBUG)

    ss = SortingStation()

    # Single-client only at the moment.
    ss.create_messenger(settings.APIKEY, settings.APISECRET)

    logger.info("Starting Thunderpush server at %s:%d",
        settings.HOST, settings.PORT)

    application.listen(settings.PORT, settings.HOST)

    try:
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        logger.info("Shutting down...")

def parse_arguments(opts, args):
    for optname in ["PORT", "HOST", "VERBOSE", "DEBUG"]:
        value = getattr(opts, optname, None)

        if not value is None:
            setattr(settings, optname, value)

    settings.APIKEY = args[0]
    settings.APISECRET = args[1]

def validate_arguments(parser, opts, args):
    if len(args) != 2:
        parser.error("incorrect number of arguments")  

def main():
    usage = "usage: %prog [options] apikey apisecret"
    parser = optparse.OptionParser(usage=usage)

    parser.add_option('-p', '--port', 
        default=settings.PORT, 
        help='binds server to custom port', 
        action="store", type="int", dest="PORT")
    
    parser.add_option('-H', '--host', 
        default=settings.HOST, 
        help='binds server to custom address',
        action="store", type="string", dest="HOST")
    
    parser.add_option('-v', '--verbose', 
        default=settings.VERBOSE, 
        help='verbose mode',
        action="store_true", dest="VERBOSE")

    parser.add_option('-d', '--debug', 
        default=settings.DEBUG, 
        help='debug mode (useful for development)',
        action="store_true", dest="DEBUG")

    opts, args = parser.parse_args()

    validate_arguments(parser, opts, args)
    parse_arguments(opts, args)
    run_app()

if __name__ == "__main__":
    main()
