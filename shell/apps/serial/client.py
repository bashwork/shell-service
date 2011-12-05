'''
'''
from datetime import datetime
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
    ''' A simple rest client wrapper around
    the httplib2 that provides the common rest verbs.
    '''

    def __init__(self, base=None):
        ''' Initializes a new instance of the RestClient

        :param base: The base uri to store for all requests
        '''
        self.base = base or "http://localhost/"
        self.client = http_client(".shell_cache")
        self.headers = {
            'content-type' : 'application/x-www-form-urlencoded',
        }
        _logger.debug('Connecting api client to %s' % base)

    def get_request(self, path):
        ''' Perform an http GET request on a resource

        :param path: The path up from the root to operate on
        :returns: The result of the operation
        '''
        _logger.debug('Getting resource %s' % path)
        resource = self.base + path
        response, content = self.client.request(resource, "GET",
            headers=self.headers)
        if response.status != 200:
            raise Exception('error getting with the api', response.content)
        return deserialize_json(content)

    def delete_request(self, path):
        ''' Perform an http DELETE request on a resource

        :param path: The path up from the root to operate on
        :returns: The result of the operation
        '''
        _logger.debug('Deleting resource %s' % path)
        resource = self.base + path
        response, content = self.client.request(resource, "DELETE",
            headers=self.headers)
        if response.status != 200:
            raise Exception('error deleting with the api', response.content)
        return response.status == 200

    def post_request(self, path, data):
        ''' Perform an http POST request on a resource

        :param path: The path up from the root to operate on
        :param data: The data to send to the resource
        :returns: The result of the operation
        '''
        _logger.debug('Creating resource %s' % path)
        resource = self.base + path
        response, content = self.client.request(resource, "POST",
            body=data, headers=self.headers)
        if response.status != 200:
            raise Exception('error creating with the api', response.content)
        return deserialize_json(content)

    def put_request(self, path, data):
        ''' Perform an http PUT request on a resource

        :param path: The path up from the root to operate on
        :param data: The data to send to the resource
        :returns: The result of the operation
        '''
        _logger.debug('Updating resource %s' % path)
        resource = self.base + path
        response, content = self.client.request(resource, "PUT",
            body=data, headers=self.headers)
        if response.status != 200:
            _logger.error(content)
            raise Exception('error updating with the api', response.content)
        return response.status == 200


class ShellClient(object):
    ''' A simple wrapper around the relevant shell
    api for use with the processing service.
    '''

    def __init__(self, base=None):
        ''' Initialize a new instance of the shell client
        '''
        self.client = RestClient(base or "http://radiant-meadow-2958.herokuapp.com/api/v1/")

    def generate_empty_reading(self, player):
        ''' A helper method to generate an empty reading for
        a given player

        :param player: The player to generate a reading for
        :returns: An empty player reading
        '''
        return {
            'player'       : player,
            'temperature'  : 0,
            'humidity'     : 0,
            'acceleration' : 0,
            'hits'         : 0,
            'date'         : str(datetime.now()),
        }

    def add_trauma(self, reading):
        ''' Adds a received trauma message to the system

        :param reading: The new reading to update or insert
        :returns: The result of the operation
        '''
        message = urlencode(reading)
        return self.client.post_request('trauma/', message)

    def update_trauma(self, reading):
        ''' Updates a received trauma message to the system

        :param reading: The new reading to update or insert
        :returns: The result of the operation
        '''
        new_date = reading.pop('date')      # keep original
        player   = reading.pop('player')    # don't change player
        message  = urlencode(reading)
        return self.client.put_request('trauma/%d' % reading['id'], message)

    def add_reading(self, reading):
        ''' Adds a received reading message to the system

        :param reading: The new reading to update or insert
        :returns: The result of the operation
        '''
        message = urlencode(reading)
        return self.client.post_request('history/', message)

    def update_reading(self, reading):
        ''' Updates a received reading message to the system

        :param reading: The new reading to update or insert
        :returns: The result of the operation
        '''
        new_date = reading.pop('date')      # keep original
        player   = reading.pop('player')    # don't change player
        message  = urlencode(reading)
        return self.client.put_request('history/%d/' % reading['id'], message)

    def get_latest_reading(self, player):
        ''' Retrieves the most recent reading for the specified player

        :param player: The player to get a reading for
        :returns: The result of the operation
        '''
        reading = self.client.get_request('player/%s/history/1' % player)
        return None if (len(reading) == 0) else reading[0]

    def get_readings(self, player, count=30):
        ''' Retrieves the most recent count readings
        for the specified player

        :param player: The player to get a reading for
        :param count: The number of readings to retreve
        :returns: The result of the operation
        '''
        return self.client.get_request('player/%s/history/%d' % (player, count))

    def get_traumas(self, player, count=30):
        ''' Retrieves the most recent count trauma
        readings for the specified player.

        :param player: The player to get a trauma reading for
        :param count: The number of trauma readings to retreve
        :returns: The result of the operation
        '''
        return self.client.get_request('player/%s/trauma/%d' % (player, count))

    def get_all_players(self):
        ''' Retrieves all the players from the service

        :returns: The collection of all the players
        '''
        return self.client.get_request('player/')

    def get_contacts(self, player):
        ''' Retrieves the contacts for the specified player

        :param player: The player to get the contacts for
        :returns: The collection of the players contacts
        '''
        contacts = self.client.get_request('player/%d/contacts' % player)
        return None if (len(contacts) == 0) else contacts


# ----------------------------------------------------------------------------- 
# Exported Types
# ----------------------------------------------------------------------------- 
__all__ = ['ShellClient']
