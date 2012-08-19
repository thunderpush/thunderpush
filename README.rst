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

JavaScript API
==============

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
    Set it to true if you want activate verbose mode.

  user
    Set it to override the client generated user id.

::
	
	Thunder.listen(handler)

Registers callback function that will receive incomming messages. You can
register as many handlers you want. Handler function should accept
one argument which is the message itself.
