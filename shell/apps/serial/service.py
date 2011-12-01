'''
service   -> wsgi      -> client stream
(thread)  -> processor -> client -> shell api
(thread)  -> processor -> queue  -> client stream
(process) -> serial    -> queue  -> processor
'''
import threading
from Queue import Queue
from gevent import pywsgi
from json import dumps as json_serialize
from client import ShellClient
from stream import SerialWatcher

# ----------------------------------------------------------------------------- 
# logging
# ----------------------------------------------------------------------------- 
import logging
_logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------- 
# processing interface
# ----------------------------------------------------------------------------- 
class ShellProcessor(threading.Thread):
    connections = [] # add/removes are atomic, no locking needed

    def __init__(self):
        ''' Initializes a new instance of the ShellProcessor
        '''
        self.watcher = SerialWatcher()
        self.client  = ShellClient()
        super(ShellProcessor, self).__init__()

    def __deliver_message(self, message):
        ''' The processing step to deliver new messages to the clients

        .. note::
        
           We deliver the message first so we can mangle the
           message reference without having to do a deep copy.

        :param message: The message to process
        '''
        message = json_serialize(message) + "\r\n"
        for queue in ShellProcessor.connections:
            queue.put_nowait(message)
    
    def __update_database(self, message):
        ''' The processing step to update the database

        :param message: The message to process
        '''
        message_type = message.pop('type', 'unknown')
        if message_type == 'trauma':
            client.add_trauma(message)
        elif message_type == 'reading':
            client.add_reading(message)
        else: _logger.debug("Unknown message: " + str(message))
    
    def run(self):
        ''' The main processor for new messages
        '''
        try:
            message_queue = self.watcher.start()
            for message in iter(message_queue.get, None):
                try:
                    self.__deliver_message(message)
                    #self.__update_database(message)
                except ex: _logger.error(ex)
        except ex: self.watcher.stop()


# ----------------------------------------------------------------------------- 
# web interface
# ----------------------------------------------------------------------------- 
def main(environ, start_response):
    ''' The main wsgi application
    '''
    queue = Queue()
    ShellProcessor.connections.append(queue)
    status = '200 OK'
    response_headers = [
        ('Content-Type', 'application/json'),
        ('Transfer-Encoding', 'chunked')
    ]
    try:
        start_response(status, response_headers)
        return iter(queue.get, None)
    except ex:
        _logger.error(ex)
        ShellProcessor.connections.remove(queue)

# ----------------------------------------------------------------------------- 
# main runner 
# ----------------------------------------------------------------------------- 
if __name__ == "__main__":
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)

    processor = ShellProcessor()
    processor.start()

    server = pywsgi.WSGIServer(('0.0.0.0', 8080), main)
    server.serve_forever()
