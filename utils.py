#!/usr/bin/env python3

from client import Client


def login(client, email, password, debug=False):
    '''
    POST auth/login
    Submits account credentials and returns an auth token
    '''
    data = {
        'email': email,
        'password': password
    }
    return client.post(endpoint='auth/login', data=data, debug=debug)


def get_account(client):
    '''
    GET account
    Retrieves account information
    '''
    return client.get(endpoint='account')


def get_all_customers(client):
    '''
    GET customers
    Retrieves all customers
    '''
    return client.get(endpoint='customers')


def get_customer(client, id):
    '''
    GET customers/{id}
    Retrieves a specific customer
    '''
    return client.get(endpoint='customers/' + str(id))

