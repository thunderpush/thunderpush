.. _topics-server-api:

===============
Server HTTP API
===============

Example of interacting with Thunderpush API using cURL::

    curl \
        -X POST \
        -H "Content-Type: application/json" \
        -H "X-Thunder-Secret-Key: secretkey" \
        --data-ascii "\"Hello World!\"" \
        http://thunder.example.com/api/1.0.0/[API key]/channels/[channel]/

All requests to the HTTP API must include `X-Thunder-Secret-Key` header that should contain the private API key.

===================
Available endpoints
===================

Sending a message to a channel
==============================

::

    POST /api/1.0.0/[API key]/channels/[channel]/

Message should be sent as the body of the request. Only valid JSON body
will be accepted.

Getting number of users online
==============================

::

    GET /api/1.0.0/[API key]/users/

Checking presence of a user
===========================

::

    GET /api/1.0.0/[API key]/users/[user id]/

Sending a message to a user
===========================

::

    POST /api/1.0.0/[API key]/users/[user id]/

Message should be sent as the body of the request. Only valid JSON body
will be accepted.

Forcing logout of a user
========================

::

    DELETE /api/1.0.0/[API key]/users/[user id]/

Always returns 204 http code.

Retrieving list of users in a channel
=====================================

::

    GET /api/1.0.0/[API key]/channels/[channel]/
