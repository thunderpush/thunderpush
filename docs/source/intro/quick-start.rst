.. _intro-quick-start:

===========
Quick start
===========

Installing Thunderpush
======================

To install Thunderpush server using pip::

    pip install thunderpush

Starting the server
===================

.. note:: Read :ref:`intro-install-deployment` for a recommended way to run Thunderpush in production environment.

Help message for Thunderpush::

    usage: thunderpush [-h] [-p PORT] [-H HOST] [-v] [-d] [-V] clientkey apikey

    positional arguments:
      clientkey             client key
      apikey                server API key

    optional arguments:
      -h, --help            show this help message and exit
      -p PORT, --port PORT  binds server to custom port
      -H HOST, --host HOST  binds server to custom address
      -v, --verbose         verbose mode
      -d, --debug           debug mode (useful for development)
      -V, --version         show program's version number and exit

To start Thunderpush on `localhost:8000` with `publickey` as apikey and `secret` as apisecret you would do following::

    thunderpush -H localhost -p 8000 publickey secret

.. _intro-install-deployment:

Deploying to production
===================================

When running an application in production, you want to make sure that it stays alive, even if a crash occurs.
A way to do it is using `supervisord <http://www.supervisord.org>`_ which is a great Python process management tool.

Assuming that you have already `installed supervisord <http://supervisord.org/installing.html>`_, add following
snippet of code to the configuration file::

    [program:thunderpush]
    command=/usr/local/bin/thunderpush -p 8000 apikey apisecret
    user=thunderpush

.. note:: We recommend creating a separate user for running Thunderpush, although it's entirely possible
    to run it as `root`, but simply removing `user=thunderpush`.

Now we're ready to start the server::

    supervisorctl start thunderpush

The server is now running at port 8000, but we want ideally to run it on port 80 alongside your web server.

To Be Continued...
