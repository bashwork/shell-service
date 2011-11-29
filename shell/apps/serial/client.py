'''
'''
from json import loads as deserialize_json
from httplib2 import Http as http_client
from shell.apps.api.models import Reading, Trauma


class RestClient(object):

    def __init__(self, base):
        ''' Initializes a new instance of the RestClient

        :param base: The base uri to store for all requests
        '''
        self.base = base
        self.client = http_client(".cache")
        self.headers = {}

    def get_request(path):
        ''' Perform an http GET request on a resource

        :param path: The path up from the root to operate on
        :returns: The result of the operation
        '''
        resource = self.base + path
        response, content = client.request(resource, "GET",
            headers=self.headers)
        if response.status != 200:
            return content
        return deserialize_json(content)

    def delete_request(path):
        ''' Perform an http DELETE request on a resource

        :param path: The path up from the root to operate on
        :returns: The result of the operation
        '''
        resource = self.base + path
        response, content = client.request(resource, "DELETE",
            headers=self.headers)
        return response.status == 200

    def post_request(path, data):
        ''' Perform an http POST request on a resource

        :param path: The path up from the root to operate on
        :param data: The data to send to the resource
        :returns: The result of the operation
        '''
        resource = self.base + path
        response, content = client.request(resource, "POST",
            data=data, headers=self.headers)
        return response.status == 200

    def put_request(path, data):
        ''' Perform an http PUT request on a resource

        :param path: The path up from the root to operate on
        :param data: The data to send to the resource
        :returns: The result of the operation
        '''
        resource = self.base + path
        response, content = client.request(resource, "PUT",
            data=data, headers=self.headers)
        return response.status == 200


class ShellClient(object):

    def __init__(self, root=None):
        ''' Initialize a new instance of the shell client
        '''
        self.client = RestClient(root or "http://radiant-meadow-2958.herokuapp.com/api/v1/")

    def add_trauma(reading):
        ''' Adds a received trauma message to the system

        :param reading: The new reading to update or insert
        :returns: The result of the operation
        '''
        message = "player=%d&acceleration=%.2f&conscious=%d" % (
            reading.player, reading.acceleration, reading.conscious)
        return self.client.post_request('trauma/', message)

    def update_reading(reading):
        ''' Adds a received reading message to the system

        :param reading: The new reading to update or insert
        :returns: The result of the operation
        '''
        exists = False # get from api and cache?
        if exists:
            message = "acceleration=%.2f&conscious=%d" % (
                reading.acceleration, reading.conscious)
            return self.client.put_request('history/%d/' % reading.player, message)
        else:
            message = "player=%d&acceleration=%.2f&conscious=%d" % (
                reading.player, reading.acceleration, reading.conscious)
            return self.client.post_request('history/', message)

