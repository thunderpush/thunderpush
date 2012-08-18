-----------
ThunderPush
-----------

ThunderPush is a Tornado and SockJS based push service. It provides
a Beaconpush (beaconpush.com) inspired HTTP API and client.

This project is in early stage of development and should not be
used in production environments.

Using the HTTP API
==================

Following examples shows usage of the API using cURL.

Sending a message to a channel
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

	curl -X POST -H "Content-Type: application/json" --data-ascii "\"Hello World!\"" http://localhost:8080/1.0.0/[secret apikey]/channel/[channel name]/
