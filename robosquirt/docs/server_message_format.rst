================================
Robosquirt Server Communications
================================

Solenoid Valve
--------------

The following messages can be sent to the Robosquirt server to control/query the a valve. They are sent as ZeroMQ messages
where the body of the message is a string  representing a JSON object.

Performing Actions
^^^^^^^^^^^^^^^^^^

The following messages instructs the robosquirt server to open the valve with the identifier ``0``.

.. code-block:: json

    {"entity": "valve",
    "identifier": 0,
    "action": "open"}

Other allowed values for ``"action"`` are ``"close"`` and ``"toggle"``. The server will return the following response on success:

.. code-block:: json

    {"entity": "valve",
    "identifier": 0,
    "action": "open",
    "succeeded": true,
    "error": null}

The server will return the following response on failure:

.. code-block:: json

    {"entity": "valve",
    "identifier": 0,
    "action": "open",
    "succeeded": false,
    "error": "There is no valve with the identifier 0."}

Here, error will be a string specifying what went wrong.

Querying State
^^^^^^^^^^^^^^

A client can also query the current state of a solenoid valve by sending the following message:

.. code-block:: json

    {"entity": "valve",
    "identifier": 0}

The following message will be returned:

.. code-block:: json

    {"entity": "valve",
    "identifier": 0,
    "state": "closed"}

Possible values for ``"state"`` are ``"open"`` and ``"unknown"`` if there is no valve with that identifier.
