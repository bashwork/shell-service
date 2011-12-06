#!/usr/bin/env python
'''
A simple serial logger for the shell firmware
messages.
'''
import sys, time, signal
from serial import Serial
from datetime import datetime
from random import randint, uniform
from multiprocessing import Process, Queue, Event 
import tinyos

# ----------------------------------------------------------------------------- 
# Logging
# ----------------------------------------------------------------------------- 
import logging
_logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------- 
# Tinyos Serial Watcher
# ----------------------------------------------------------------------------- 
class TinyosHistoryMessage(tinyos.Packet):

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
        values = [(i<<8 | j) for (i,j) in zip(self.readings[::2], self.readings[1::10])]
        return {
            'player'       : self.id,
            'type'         :'reading',
            'temperature'  : values[1],
            'humidity'     : values[2],
            'acceleration' : values[3] + values[4],
            'hits'         : values[0],
            'date'         : str(datetime.now()),
        }

    @classmethod
    def random(cls, player):
        ''' Returns a random message used for testing
        '''
        return {
            'player'       : player,
            'type'         :'reading',
            'temperature'  : uniform(97, 100),
            'humidity'     : uniform(97, 100),
            'acceleration' : uniform(0, 100),
            'hits'         : randint(0, 5),
            'date'         : str(datetime.now()),
        }


class TinyosTraumaMessage(tinyos.Packet):

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
            'date'         : str(datetime.now()),
            'conscious'    : True,  # this is validated later
            'comments'     : '',    # this is updated later
        }

    @classmethod
    def random(cls, player):
        ''' Returns a random message used for testing
        '''
        return {
            'player'       : player,
            'type'         :'trauma',
            'acceleration' : uniform(90, 110),
            'date'         : str(datetime.now()),
            'conscious'    : True,
            'comments'     : '',
        }


class TinyosWatcher(object):

    def __init__(self, *args, **kwargs):
        ''' Initializes a new instance of the TinyosWatcher

        :param port: The serial port to read on (default serial@/dev/ttyUSB0:57600)
        '''
        sys.argv = ['', kwargs.get('port', "serial@/dev/ttyUSB0:57600")]
        self.client = tinyos.AM() # hack, I blame tinyos

    def __iter__(self):
        ''' Returns an instance of the current iterator
       
        :returns: The iterator instance
        '''
        return self

    def __parse(self, packet):
        ''' A helper method to parse the packet

        :param packet: The packet to decode
        :returns: The decoded packet
        '''
        message = None
        if packet and (packet.type == TinyosHistoryMessage.Type):
            message = TinyosHistoryMessage(packet.data).decode()
        elif packet and (packet.type == TinyosTraumaMessage.Type):
            message = TinyosTraumaMessage(packet.data).decode()
        else: _logger.debug(packet)
        return message

    def close(self):
        ''' Close the underlying watcher handle
        '''
        pass

    def next(self):
        ''' Returns the next message from the iterator
       
        :returns: The next value of the iterator 
        '''
        packet  = self.client.read()
        return self.__parse(packet)

# ----------------------------------------------------------------------------- 
# Arduino serial watcher
# ----------------------------------------------------------------------------- 
class ArduinoTraumaMessage(object):
    ''' Represents an aduino trauma message
    '''

    Type = 'trauma'

    @classmethod
    def decode(cls, message):
        ''' Specifically parse a trauma message

        :param message: The message to populate with
        :returns: The parsed message
        '''
        return {
            'player'       : message['id'],
            'type'         :'trauma',
            'acceleration' : float(message['accel']),
            'date'         : str(datetime.now()),
            'conscious'    : True,
            'comments'     : '',
        }

class ArduinoHistoryMessage(object):
    ''' Represents an aduino history message
    '''

    Type = 'reading'

    @classmethod
    def decode(cls, message):
        ''' Specifically parse a reading message

        :param message: The message to populate with
        :returns: The parsed message
        '''
        return {
            'player'       : message['id'],
            'type'         :'reading',
            'temperature'  : uniform(97, 100), # the arduino doesn't have this
            'humidity'     : uniform(97, 100), # the arduino doesn't have this
            'acceleration' : message['accel'],
            'hits'         : message['hits'],
            'date'         : str(datetime.now()),
        }


class ArduinoWatcher(object):
    ''' A simple iterator wrapper around reading from an
    arduino. For this we simply use a serial line reader.
    '''

    def __init__(self, *args, **kwargs):
        ''' Initializes a new instance of the TinyosWatcher

        :param port: The serial port to read from
        :param baudrate: The baudrate to read with
        '''
        self.client = Serial(**kwargs)

    def __iter__(self):
        ''' Returns an instance of the current iterator
       
        :returns: The iterator instance
        '''
        return self

    def __parse(self, packet):
        ''' A helper method to parse the packet

        :param packet: The packet to decode
        :returns: The decoded packet
        '''
        result  = None
        message = dict(p.split(':') for p in packet.split(','))
        message_type = message.get('type', None)
        if message_type == ArduinoTraumaMessage.Type:
            result = ArduinoTraumaMessage.decode(message)
        elif message_type == ArduinoHistoryMessage:
            result = ArduinoHistoryMessage.decode(message)
        else: _logger.debug("invalid message: " + packet)
        return result

    def close(self):
        ''' Close the underlying watcher handle
        '''
        self.client.close()

    def next(self):
        ''' Returns the next value from the iterator
       
       :returns: The next value of the iterator 
        '''
        packet = self.client.readline()
        return self.__parse(packet)
        

# ----------------------------------------------------------------------------- 
# Main Runner
# ----------------------------------------------------------------------------- 
class SerialWatcher(object):
    
    def __init__(self, port=None, watcher='arduino'):
        ''' Initialize a new instance of the class
        '''
        self.queue = Queue()
        self.event = Event()
        arguments = (self.event, self.queue, port, watcher)
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
    def __watcher(cls, event, queue, port, watcher):
        ''' The main runner for pulling messages off the serial
            bus and throwing them into the database
        '''
        _logger.info("initialized the serial monitor")
        if watcher == 'arduino':
            client = ArduinoWatcher(port=port, timeout=5)
        else: client = TinyosWatcher(port)
    
        while not event.is_set():
            for message in client:
                if message: queue.put(message)
        client.close()
        _logger.info("exited the serial monitor")


# ----------------------------------------------------------------------------- 
# Exported Types
# ----------------------------------------------------------------------------- 
__all__ = ['SerialWatcher']

# ----------------------------------------------------------------------------- 
# Test Runner
# ----------------------------------------------------------------------------- 
if __name__ == "__main__":
    watcher = SerialWatcher()

    def signal_handler(signal, frame):
        ''' Make sure we can clean up correctly '''
        watcher.stop()
        sys.exit(0)
    signal.signal(signal.SIGINT, signal_handler)

    try:
        queue = watcher.start()
        for message in iter(queue.get, None):
            print message
    except Exception as ex:
        _logger.exception("stream exiting")

