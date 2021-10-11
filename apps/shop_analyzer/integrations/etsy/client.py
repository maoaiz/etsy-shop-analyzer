import logging
import math

from django.conf import settings
from ..rest_client import RestClient


class EtsyClient(RestClient):
    """
    Wraps calls to Etsy's public API

    Parameters
    ----------
    key_string : str
        Etsy key string.
    verbose : boolean, default=False
        If True, logs the information of each request for debugging. It is
        also possible to activate it using an environment variable
        DEBUG_RESTCLIENT. The environment variable takes precedence over
        the parameter.
    """

    def __init__(self, key_string, verbose=False):

        self.logger = logging.getLogger(__name__)

        api_url = 'https://openapi.etsy.com/v3/application'

        super().__init__(api_url, verbose=verbose)

        self.timeout = (
            settings.CLIENT_CONNECT_TIMEOUT, settings.CLIENT_READ_TIMEOUT
        )

        self.key_string = key_string
        self.headers['x-api-key'] = self.key_string

    def _request_all(self, endpoint, limit=100, offset=0):
        """
            Encapsulates all the logic to iterate over the pages returning
            a generator with the requests

        Parameters
        ----------
        endpoint : str
            Etsy's endpoint
        params : dict
            The dictionary with the params to send to Etsy

        Returns
        ----------
        result : generator
            A generator with all the objects
        """

        params = {'limit': limit, 'offset': offset}

        status_code, response = self.perform_request(endpoint, params=params)
        # Response is a dict with 2 keys:
        # 1. 'count'. Number of items returned.
        # 2. 'results'. A list with the data

        # Defines the total number of objects that match a query.
        count = int(response.get('count', '0'))

        self.logger.debug(
            f'Total objects (count): {count} limit: {limit} offset: {offset}'
        )

        offset = int(offset)

        data = response.get('results', [])

        for _d in data:
            # We send every single record to the generator
            yield _d

        # We calculate the number of pages
        total_pages = math.ceil((count - offset) / limit)

        # We iterate over the rest of pages
        for next_page in range(1, total_pages):

            # the offset should incremet according to limit param.
            offset = next_page * limit
            params['offset'] = offset

            self.logger.debug(f"New request to {endpoint}. Offset: {offset}")

            status_code, response = self.perform_request(
                endpoint, params=params
            )

            data = response.get('results', [])

            for _d in data:
                # Return every single record (dict) (in the data list)
                # to the generator
                yield _d

    def get_shops_by_name(self, shop_name):
        """
        Returns a shop list with the shops data.
        A shop is a store in Etsy platform.
        """

        self.logger.debug(f'Getting shops data by name "{shop_name}"')
        return self._request_all(f'/shops?shop_name={shop_name}')

    def get_shop_by_id(self, shop_id):
        """
        Returns a single shop.
        A shop is a store in Etsy platform.
        """

        self.logger.debug(f'Getting shop by id: "{shop_id}"')
        _, response = self.perform_request(f'/shops/{shop_id}')
        return response

    def get_items_by_shop(self, shop_id):
        """
        Returns a shop list with the shops data.
        A shop is a store in Etsy platform.

        We are usign the public API, only public items can be returned.
        """

        self.logger.debug(f'Getting items for shop "{shop_id}"')
        return self._request_all(f'/shops/{shop_id}/listings/active')
