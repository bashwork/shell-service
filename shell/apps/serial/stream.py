#!/usr/bin/env python
'''
A simple serial logger for the shell firmware
messages.
'''
import sys, time
import tinyos
from multiprocessing import Process, Queue, Event 

# ----------------------------------------------------------------------------- 
# Logging
# ----------------------------------------------------------------------------- 
import logging
_logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------- 
# Classes
# ----------------------------------------------------------------------------- 
class HistoryMessage(tinyos.Packet):

    Type = 0x93

    def __init__(self, packet = None):
        ''' Initialize a new instance of the ShellMessage

        :param packet: The packet to parse
        '''
        settings = [
            ('version',  'int', 2),
            ('id',       'int', 2),
            ('count',    'int', 2),
            ('readings', 'blob', None)]
        tinyos.Packet.__init__(self, settings, packet)

    def decode(self):
        ''' Return the parsed data packet

        :returns: The parsed data packet as a dict
        '''
        values = [(i<<8 | j) for (i,j) in zip(self.readings[::2], self.readings[1::4])]
        return {
            'player'       : self.id,
            'type'         :'reading',
            'temperature'  : 97.5,
            'humidity'     : 97.5,
            'acceleration' : values[0],
            'hits'         : values[1],
            'date'         : datetime.now(),
        }


class TraumaMessage(tinyos.Packet):

    Type = 0x94

    def __init__(self, packet = None):
        ''' Initialize a new instance of the ShellMessage

        :param packet: The packet to parse
        '''
        settings = [
            ('version',  'int', 2),
            ('id',       'int', 2),
            ('count',    'int', 2),
            ('readings', 'blob', None)]
        tinyos.Packet.__init__(self, settings, packet)

    def decode(self):
        ''' Return the parsed data packet

        :returns: The parsed data packet as a dict
        '''
        values = [(i<<8 | j) for (i,j) in zip(self.readings[::2], self.readings[1::2])]
        return {
            'player'       : self.id,
            'type'         :'trauma',
            'acceleration' : values[0],
            'date'         : datetime.now(),
            'comments'     : '',
        }


# ----------------------------------------------------------------------------- 
# Main Runner
# ----------------------------------------------------------------------------- 
class SerialWatcher(object):
    
    def __init__(self):
        ''' Initialize a new instance of the class
        '''
        self.queue = Queue()
        self.event = Event()
        arguments = (self.event, self.queue)
        self.process = Process(target=self.__watcher, args=arguments)

    def start(self):
        ''' Start the processor running

        :returns: The intermessage queue to read from
        '''
        _logger.info("starting the serial monitor")
        self.event.clear()
        self.process.start()
        return self.queue

    def stop(self):
        ''' Stop the processor from running
        '''
        _logger.info("stoping the serial monitor")
        self.event.set()
        self.process.join(1)
        if self.process.is_alive():
            self.process.terminate()

    @classmethod
    def __watcher(cls, event, queue, port="serial@/dev/ttyUSB0:57600"):
        ''' The main runner for pulling messages off the serial
            bus and throwing them into the database
        '''
        sys.argv = ['', port] # hack, I blame tinyos
        #messages = tinyos.AM()
    
        _logger.info("initialized the serial monitor")
        while not event.is_set():
            queue.put({'type':'unknown', 'data':'hello world'})
            time.sleep(1)
        _logger.info("exited the serial monitor")

            #packet = messages.read()
            #if packet and (packet.type == HistoryMessage.Type):
            #    message = HistoryMessage(p.data)
            #    queue.put(message.decode)
            #elif packet and (packet.type == TraumaMessage.Type):
            #    message = TraumaMessage(p.data)
            #    queue.put(message.decode)
            #else: _logger.debug(packet)


# ----------------------------------------------------------------------------- 
# Exported Types
# ----------------------------------------------------------------------------- 
__all__ = ['SerialWatcher']
