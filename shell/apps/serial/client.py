'''
'''
from urllib import urlencode
from json import loads as deserialize_json
from httplib2 import Http as http_client

# ----------------------------------------------------------------------------- 
# logging
# ----------------------------------------------------------------------------- 
import logging
_logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------- 
# classes
# ----------------------------------------------------------------------------- 
class RestClient(object):

    def __init__(self, base):
        ''' Initializes a new instance of the RestClient

        :param base: The base uri to store for all requests
        '''
        self.base = base
        self.client = http_client(".cache")
        self.headers = {'content-type':'application/x-www-form-urlencoded'}

    def get_request(self, path):
        ''' Perform an http GET request on a resource

        :param path: The path up from the root to operate on
        :returns: The result of the operation
        '''
        resource = self.base + path
        response, content = self.client.request(resource, "GET",
            headers=self.headers)
        if response.status != 200:
            return content
        return deserialize_json(content)

    def delete_request(self, path):
        ''' Perform an http DELETE request on a resource

        :param path: The path up from the root to operate on
        :returns: The result of the operation
        '''
        resource = self.base + path
        response, content = self.client.request(resource, "DELETE",
            headers=self.headers)
        return response.status == 200

    def post_request(self, path, data):
        ''' Perform an http POST request on a resource

        :param path: The path up from the root to operate on
        :param data: The data to send to the resource
        :returns: The result of the operation
        '''
        resource = self.base + path
        response, content = self.client.request(resource, "POST",
            body=data, headers=self.headers)
        return response.status == 200

    def put_request(self, path, data):
        ''' Perform an http PUT request on a resource

        :param path: The path up from the root to operate on
        :param data: The data to send to the resource
        :returns: The result of the operation
        '''
        resource = self.base + path
        response, content = self.client.request(resource, "PUT",
            body=data, headers=self.headers)
        return response.status == 200


class ShellClient(object):

    def __init__(self, root=None):
        ''' Initialize a new instance of the shell client
        '''
        self.date_cache = {}
        self.client = RestClient(root or "http://radiant-meadow-2958.herokuapp.com/api/v1/")

    def add_trauma(self, reading):
        ''' Adds a received trauma message to the system

        :param reading: The new reading to update or insert
        :returns: The result of the operation
        '''
        message = urlencode(reading)
        return self.client.post_request('trauma/', message)

    def add_reading(self, reading):
        ''' Adds a received reading message to the system

        :param reading: The new reading to update or insert
        :returns: The result of the operation
        '''
        if player_reading_exists(reading['player']):
            new_date = reading.pop('date') # keep original
            message = urlencode(reading)
            return self.client.put_request('history/%d/' % reading.player, message)
        # we have to add a new entry for today
        message = urlencode(reading)
        return self.client.post_request('history/', message)

    def player_reading_exist(self, player):
        ''' Checks to see if we have an existing reading for today

        :param player: The player to check for a current reading for
        :returns: The result of the operation
        '''
        today = str(date.today())
        if self.date_cache.get(player, None) == today:
            return True
        date = self.get_reading(player)['date'].split(' ')[0]
        self.date_cache['player'] = date
        return True if (date == today) else False

    def get_reading(self, player):
        ''' Retrieves the most recent reading for the specified player

        :param player: The player to get a reading for
        :returns: The result of the operation
        '''
        return self.client.get_request('player/%s/history/1' % player)[0]
