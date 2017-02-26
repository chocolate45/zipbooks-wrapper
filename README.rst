Zipbooks Python Wrapper
=======================

A simple Python wrapper for the [Zipbooks API 0.1.0](https://developer.zipbooks.com).

Requirements
------------

[Requests: HTTP for Humans](http://docs.python-requests.org/en/master/)

Usage
-----
    # Create a client instance
    client = Client()

    # Login to save your JSON web token for authentication to your client
    login(client=client, email='you@example.com', password='YourPassword')

    # Retrieve account information
    response = client.get(endpoint='account', debug=True)


