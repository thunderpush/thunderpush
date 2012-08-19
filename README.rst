-----------
Thunderpush
-----------

Thunderpush is a Tornado and SockJS based push service. It provides
a Beaconpush (beaconpush.com) inspired HTTP API and client.

This project is in early stage of development and should not be
used in production environments.

Using the HTTP API
==================

Example of interacting with Thunderpush API using cURL::

	curl \
		-X POST \
		-H "Content-Type: application/json" \
		-H "X-Thunder-Secret-Key: secretkey" \
		--data-ascii "\"Hello World!\"" \
		http://localhost:8080/1.0.0/[API key]/channel/[channel]/

Sending a message to a channel::
	
	POST /1.0.0/[API key]/channels/[channel]/

Getting number of users online::

	GET /1.0.0/[API key]/users/

Checking presence of a user::

	GET /1.0.0/[API key]/users/[user id]/

Returns 200 or 404 depending on if the user is online or not.

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
	Thunder.listen(function(e) { alert(e.data) });
	</script>

This code is all you need to do to start receive messages pushed to the client
from your Thunderpush server. As you can see, we instructed Thunder client
to display logs, which can be helpful for debugging your application.

For more examples of how to use Thunderpush, look into *examples/*.

JavaScript client API
=====================

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

::
	
	Thunder.listen(handler)

Registers callback function that will receive incomming messages. You can
register as many handlers you want. Handler function should accept
one argument which is the message itself.
