#!/usr/bin/env python3

import time
import json
import requests


class API(object):

    def __init__(self, base_url, token, max_retries=5, verify=True):
        assert base_url
        self.base_url = base_url
        self.max_retries = max_retries
        self.verify = verify
        self.requests = requests
        self.session = self.requests.Session()

    def _print_request(self, request):
        print('{}\n{}\n{}\n\n{}\n{}'.format(
            '----------- HTTP Request -----------',
            request.method + ' ' + request.url,
            '\n'.join('{}: {}'.format(k, v) for k, v in request.headers.items()),
            request.body or '',
            '----------- /HTTP Request -----------'))

    def dispatch(self, method_name, endpoint, **kwargs):
        data = kwargs.pop('data', None)
        debug = kwargs.pop('debug', False)

        for retry_count in range(self.max_retries):
            try:
                kwargs.update({
                    'json': data
                })
                request = requests.Request(
                    method_name,
                    self.base_url + endpoint,
                    **kwargs
                )
                prepped_request = self.session.prepare_request(request)
                if debug:
                    self._print_request(prepped_request)
                response = self.session.send(prepped_request,
                                             verify=self.verify)
                response.raise_for_status()
                if endpoint == 'auth/login/':
                    response_dict = json.loads(response.text)
                    self.token = response_dict['token']
                    self.session.headers.update(
                        {
                            'Authorization': 'Bearer ' + self.token,
                            'Content-Type': 'application/x-www-form-urlencoded'
                        }
                    )
                    return self.token
                return response
            except requests.exceptions.ConnectionError:
                if (retry_count + 1 == self.max_retries):
                    raise
                time.sleep(2)
            else:
                break

    def login(self, data, **kwargs):
        endpoint = 'auth/login'
        kwargs.update({'data': data})
        return self.dispatch('post', endpoint + '/', **kwargs)

    def get(self, endpoint, params=None, **kwargs):
        kwargs.update({'params': params})
        return self.dispatch('get', endpoint + '/', **kwargs)

    def post(self, endpoint, data, **kwargs):
        kwargs.update({'data': data})
        return self.dispatch('post', endpoint + '/', **kwargs)

    def put(self, endpoint, data, **kwargs):
        kwargs.update({'data': data})
        return self.dispatch('put', endpoint + '/', **kwargs)

    def delete(self, endpoint, **kwargs):
        return self.dispatch('delete', endpoint + '/', **kwargs)


class Client(API):
    def __init__(self, token=None, max_retries=5):
        base_url = 'https://api.zipbooks.com/v1/'
        verify = True
        super(Client, self).__init__(
            base_url, token, max_retries=max_retries, verify=verify)
