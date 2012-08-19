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
	
	POST /1.0.0/[API key]/channels/[channel]

Getting number of users online::

	GET /1.0.0/[API key]/users
