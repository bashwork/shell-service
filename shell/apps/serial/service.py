'''
service   -> wsgi      -> client stream
(thread)  -> processor -> client -> shell api
(thread)  -> processor -> queue  -> client stream
(process) -> serial    -> queue  -> processor
'''
import signal, sys, threading
from datetime import date
from Queue import Queue
from gevent import pywsgi
from json import dumps as json_serialize
from client import ShellClient
from stream import DeviceWatcher
from twilio.rest import TwilioRestClient

# ----------------------------------------------------------------------------- 
# logging
# ----------------------------------------------------------------------------- 
import logging
_logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------- 
# processing interface
# ----------------------------------------------------------------------------- 
class PlayerStatus(object):
    ''' An enumeration representing the player status values.
    Redefined here so we are not reliant upon the api.
    '''
    Unknown    = 0
    Normal     = 1
    Warning    = 2
    Emergency  = 3


class IterableQueue(Queue):
    ''' A simple queue wrapper that implements
    iterable and auto registration, deregistration with
    my handler.
    '''

    def __init__(self):
        ''' Initializes a new instance of the IterableQueue
        and registers this with the processor.
        '''
        Queue.__init__(self) # Queue is an old style class
        ShellProcessor.connections.append(self)
        _logger.debug("Registering a client for processing")

    def __iter__(self):
        ''' Gets the iterator for this instance.

        :returns: a handle to a new iterator
        '''
        return iter(self.get, None)

    def close(self):
        ''' Close this queue down and unregister it
        from the processor.
        '''
        self.put(None)
        self.task_done()
        ShellProcessor.connections.remove(self)
        _logger.debug("Unregistering a client from processing")


class ShellProcessor(threading.Thread):
    ''' This is the shell message processing service
    ''' 
    connections    = [] # add/removes are atomic, no locking needed

    def __init__(self, **kwargs):
        ''' Initializes a new instance of the ShellProcessor
        '''
        super(ShellProcessor, self).__init__()
        self.halt_event = threading.Event()
        self.watcher    = DeviceWatcher(kwargs.get('device_port'), kwargs.get('device_type'))
        self.client     = ShellClient(kwargs.get('service_base'))
        self.twilio     = TwilioRestClient(kwargs.get('twilio_account'), kwargs.get('twilio_token'))
        self.__initialize_caches()

    def __initialize_caches(self):
        ''' Initialize the player cache
        '''
        players = self.client.get_all_players()
        self.player_cache  = dict((player['id'], player) for player in players)
        self.reading_cache = {}

    def __send_alert_message(self, player):
        ''' Send an alert message to 

        :param player: The player to send a mesasge to
        '''
        player = self.player_cache[player]
        if (not player.get('contacted', False)) and (len(player['contacts']) > 0):
            result  = True
            params  = (player['firstname'], player['lastname'])
            message = "%s %s experienced a possible tramatic injury, please follow up." % params
            numbers = [contact['phone'] for contact in player['contacts']]
            for number in numbers:
                _logger.info("Sending emergency text to %s", number)
                sms = self.twilio.sms.messages.create(to=number, from_='4155992671', body=message)
                result &= (sms.status != "failed")
            player['contacted'] = result # don't send any more messages if all successful

    def __get_reading_today(self, player):
        ''' Checks to see if we have an existing reading for today

        :param player: The player to check for a current reading for
        :returns: The result of the operation
        '''
        # we are already cached, just return that
        today = str(date.today())
        if self.reading_cache.get(player, {'short_date':''})['short_date'] == today:
            return self.reading_cache[player]

        # we haven't cached yet, get and check latest reading
        reading = self.client.get_latest_reading(player)
        if reading != None:
            reading['short_date'] = reading['date'].split(' ')[0]
            if reading['short_date'] == today:
                self.reading_cache[player] = reading
                return reading

        # we don't have a reading for today, create it
        reading = self.client.generate_empty_reading(player)
        reading = self.client.add_reading(reading)
        reading['short_date'] = today
        self.reading_cache[player] = reading
        return reading

    def __update_player_status(self, player, status):
        ''' A helper method to simply update the player status

        :param player: The player to check for a current reading for
        :returns: The result of the operation
        '''
        reading = self.__get_reading_today(player)
        self.client.update_reading({
            'id'     : reading['id'],
            'status' : PlayerStatus.Emergency,
            'date'   : reading['date'],
            'player' : player,
        })

    def __process_message(self, message):
        ''' Merges the newest reading data and the current value
        in the cache.

        :param message: The message to merge with the cache
        :returns: The merged message
        '''
        if message['type'] == 'reading':
            reading = self.__get_reading_today(message['player'])
            message['id'] = reading['id'] 
            message['hits'] = reading['hits'] = (message['hits'] + int(reading['hits']))
            message['acceleration'] = reading['acceleration'] = (message['acceleration'] + float(reading['acceleration']))
            reading['humidity'] = message['humidity'] 
            reading['temperature'] = message['temperature'] 
        elif message['type'] == 'trauma': pass # the trauma message is merged on the sensor

    def __determine_status(self, message):
        ''' The processing step to determine the status of the player

        The rules are as follows:

        1. If no readings are found, the player status is unknown
        2. If the hits >=25 or the acceleration is >= 100, the status is warning
        3. If the hits >= 50 or the acceleration is >= 200, the status is emergency
        4. Otherwise the status is normal

        :param message: The message to process
        '''
        if message['type'] == 'reading':
            if (message['hits'] >= 50) or (message['acceleration'] > 200) or (message['temperature'] > 100):
                message['status'] = PlayerStatus.Emergency
                self.__send_alert_message(message['player'])
            elif (message['hits'] >= 25) or (message['acceleration'] > 100):
                message['status'] = PlayerStatus.Warning
            else: message['status'] = PlayerStatus.Normal
        elif message['type'] == 'trauma': # a trauma will throw the player into an emergency status
            self.__update_player_status(message['player'], PlayerStatus.Emergency)
            self.__send_alert_message(message['player'])

    def __deliver_message(self, message):
        ''' The processing step to deliver new messages to the clients

        .. note::
        
           We deliver the message first so we can mangle the
           message reference without having to do a deep copy.

        :param message: The message to process
        '''
        client_count = len(ShellProcessor.connections)
        if client_count > 0: # don't waste time if there are no clients
            _logger.debug("delivering message to %d clients" % client_count)
            message = json_serialize(message) + "\r\n"
            for queue in ShellProcessor.connections:
                queue.put_nowait(message)
    
    def __update_database(self, message):
        ''' The processing step to update the database

        :param message: The message to process
        '''
        message_type = message.pop('type', 'unknown')
        if message_type == 'trauma': self.client.add_trauma(message)
        elif message_type == 'reading': self.client.update_reading(message)
        else: _logger.error("Unknown message: " + str(message))

    def stop(self):
        ''' Stop the processing service from running '''
        _logger.info("processing sevice was told to stop")
        self.halt_event.set()
        self.watcher.stop()
    
    def run(self):
        ''' The main processor for new messages '''
        try:
            _logger.info("processing sevice starting")
            message_queue = self.watcher.start()
            for message in iter(message_queue.get, None):
                if self.halt_event.is_set(): raise Exception("Stopping")
                try:
                    _logger.debug(str(message))
                    self.__process_message(message)
                    self.__determine_status(message)
                    self.__deliver_message(message)
                    self.__update_database(message)
                except Exception as ex:
                    _logger.exception("error processing message")
        except Exception as ex:
            _logger.exception("exiting the processing thread")
            self.stop() # just in case...


# ----------------------------------------------------------------------------- 
# web interface
# ----------------------------------------------------------------------------- 
def main(environ, start_response):
    ''' The main wsgi application
    '''
    queue = IterableQueue()
    status = '200 OK'
    response_headers = [
        ('Content-Type', 'application/json'),
        ('Transfer-Encoding', 'chunked')
    ]
    try:
        start_response(status, response_headers)
        return queue
    except Exception as ex:
        _logger.exception("removing client from processing", ex)
        ShellProcessor.connections.remove(queue)

# ----------------------------------------------------------------------------- 
# main runner 
# ----------------------------------------------------------------------------- 
# Use the twisted tac file to run as gevent steals the signals...I don't know
# how to clean up now.
# ----------------------------------------------------------------------------- 
if __name__ == "__main__":

    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)

    processor = ShellProcessor()
    processor.start()

    server = pywsgi.WSGIServer(('0.0.0.0', 8080), main)

    def signal_handler(signal, frame):
        ''' Make sure we can clean up correctly '''
        server.stop()
        processor.stop()
        processor.join()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    server.serve_forever() # never returns
