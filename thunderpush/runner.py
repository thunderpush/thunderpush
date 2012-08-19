from thunderpush.sortingstation import SortingStation
from thunderpush.handler import ThunderSocketHandler
from thunderpush import api

from sockjs.tornado import SockJSRouter

import tornado.ioloop


def main():
    ThunderRouter = SockJSRouter(ThunderSocketHandler, "/connect")

    # api urls
    urls = [
        (r"/1\.0\.0/(?P<apikey>.+)/users/", api.UserCountHandler),
        (r"/1\.0\.0/(?P<apikey>.+)/users/(?P<user>.+)/", api.UserHandler),
        (r"/1\.0\.0/(?P<apikey>.+)/channels/(?P<channel>.+)/", api.ChannelHandler),
    ]

    # include sockjs urls
    urls += ThunderRouter.urls

    application = tornado.web.Application(urls, debug=True)

    ss = SortingStation()
    ss.create_messenger("key", "secretkey")

    application.listen(8080)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
