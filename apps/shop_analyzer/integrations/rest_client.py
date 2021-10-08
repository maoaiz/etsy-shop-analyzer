import json
import logging
import os

import requests
from django.conf import settings


class RestClient:
    """
    Base class to perform REST request to any API
    Parameters
    ----------
    base_url : str
        The base url or base endpoint for the REST API
    verbose : boolean, default=False
        If True, logs the information of each request for debugging. It is
        also possible to activate it using an environment variable
        DEBUG_RESTCLIENT. The environment variable takes precedence over
        the parameter.
    """

    def __init__(self, base_url, verbose=False):
        self.base_url = base_url
        self.verbose = os.getenv('DEBUG_RESTCLIENT') == 'true' or verbose
        self.headers = {'Content-type': 'application/json'}

        self.timeout = (settings.CLIENT_CONNECT_TIMEOUT, settings.CLIENT_READ_TIMEOUT)

        # this is the HTTP client, by default we use python resquests,
        # but any RestClient can define it overriding this method
        self.client = requests
        if self.verbose:
            self._logger = logging.getLogger('RestClient')

    def perform_request(self, endpoint, params={}, method='GET'):
        """
            Performs a request to the given endpoint.
        Parameters
        ----------
        endpoint : str
            The endpoint to consume
        params : dict, default={}
            The params for the request in a dict.
        method : str, {'GET', 'POST', 'PUT', 'PATCH', 'DELETE'}, default='GET'.
            The HTTP method for the request
        Returns
        -------
        status : int
            The HTTP status returned by the server
        payload : object
            The payload returned by the server
        """
        url = self.base_url + endpoint
        if self.verbose:
            self._logger.debug(f'Performing {method} to {url} with {params}')

        if method == 'GET':
            r = self.client.get(url, params=params, headers=self.headers, timeout=self.timeout)
        else:
            r = self.client.request(method, url, json=params, headers=self.headers, timeout=self.timeout)
        if self.verbose:
            self._logger.debug(f'Response:\n{r.text}')
        try:
            response_json = r.json()
            return r.status_code, response_json
        except json.decoder.JSONDecodeError as e:
            self._logger.warning(f'Performing {method} to {url} with {params}')
            self._logger.warning('Bad response: [%s] [%s]' % (r.status_code, r.text))
            raise (e)
