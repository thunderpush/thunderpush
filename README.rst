.. image:: http://i.imgur.com/CgGL5eU.png
------

.. image:: https://badge.fury.io/py/thunderpush.png
	:target: http://badge.fury.io/py/thunderpush

.. image:: https://secure.travis-ci.org/thunderpush/thunderpush.png?branch=master
	:target: http://travis-ci.org/thunderpush/thunderpush

Thunderpush is a Tornado and SockJS based push service. It provides
a Beaconpush (beaconpush.com) inspired HTTP API and client.

Install
=======

::

	pip install thunderpush

Using Docker
============

::

        docker run -d -p 8080:8080 \
            -e PUBLIC_KEY=public \
            -e PRIVATE_KEY=secret \
            kjagiello/thunderpush

Usage
=====

::

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

JavaScript client
=================

In order to use provided by Thunderpush client, you need to include following
lines on your webpage.

::

	<script src="http://cdn.sockjs.org/sockjs-0.3.min.js"></script>
	<script src="thunderpush.js"></script>

The only thing you have to do now is to make a connection to your Thunderpush
server in following way::

	<script type="text/javascript">
	Thunder.connect("thunder.example.com", "apikey", ["testchannel"], {log: true});
	Thunder.listen(function(message) { alert(message); });
	</script>

This code is all you need to do to start receive messages pushed to the client
from your Thunderpush server. As you can see, we instructed Thunder client
to display logs, which can be helpful for debugging your application.

For more examples of how to use Thunderpush, look into `examples <https://github.com/thunderpush/thunderpush/tree/master/examples>`_.

Open-source libraries for communicating with the HTTP API
=========================================================

Python: `python-thunderclient <https://github.com/thunderpush/python-thunderclient>`_

PHP: `php-thunderclient <https://github.com/thunderpush/php-thunderclient>`_

Java: `java-thunderclient <https://github.com/Sim00n/java-thunderclient>`_

Hubot: `hubot-thunderpush <https://github.com/thunderpush/hubot-thunderpush>`_

Ruby: `thunderpush-gem <https://github.com/welingtonsampaio/thunderpush-gem>`_

.NET: `ThunderClient.Net <https://github.com/primediabroadcasting/ThunderClient.Net>`_

Using the HTTP API
==================

Example of interacting with Thunderpush API using cURL::

	curl \
		-X POST \
		-H "Content-Type: application/json" \
		-H "X-Thunder-Secret-Key: secretkey" \
		--data-ascii "\"Hello World!\"" \
		http://thunder.example.com/api/1.0.0/[API key]/channels/[channel]/

All requests to the HTTP API must provide *X-Thunder-Secret-Key* header that
should contain the private API key.

Sending a message to a channel
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

	POST /api/1.0.0/[API key]/channels/[channel]/

Message should be sent as the body of the request. Only valid JSON body
will be accepted.

Getting number of users online
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

	GET /api/1.0.0/[API key]/users/

Checking presence of a user
^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

	GET /api/1.0.0/[API key]/users/[user id]/

Sending a message to a user
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

	POST /api/1.0.0/[API key]/users/[user id]/

Message should be sent as the body of the request. Only valid JSON body
will be accepted.

Forcing logout of a user
^^^^^^^^^^^^^^^^^^^^^^^^

::

	DELETE /api/1.0.0/[API key]/users/[user id]/

Always returns 204 http code.

Retrieving list of users in a channel
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

	GET /api/1.0.0/[API key]/channels/[channel]/

JavaScript client API
=====================

Connecting to the server
^^^^^^^^^^^^^^^^^^^^^^^^

::

	Thunder.connect(server, apiKey, channels, options)

Connects to the Thunderpush server and starts listening for incomming
messages.

server
  Adress of your Thunderpush server.

apiKey
  Public api key.

channels
  Array of channels you want to subscribe to.

options
  Object with optional settings you may pass to Thunder:

  log
	Set it to true if you want to activate verbose mode. This will turn on
	SockJS logs as well.

  user
	Set it to override the client generated user id.

	protocol
	Set it to "https" if you want to use it instead of "http".

Listening for messages
^^^^^^^^^^^^^^^^^^^^^^

::

	Thunder.listen(handler)

Registers callback function that will receive incomming messages. You can
register as many handlers you want. Handler function should accept
one argument which is the message itself.

Getting high CPU usage?
^^^^^^^^^^^^^^^^^^^^^^^

Before giving up on thunderpush, check it's logs and look for
errors like this one `error: [Errno 24] Too many open files`. If you're seeing them,
it means that you've reached the limit of open file descriptors on your system.
The only thing you need to do is to raise the limit. Following SO answer will
tell you how to do it: http://stackoverflow.com/a/4578356/250162 Then simply
restart thunderpush, forget about the problem and get a cold one!
