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
            'temperature'  : float(values[1]),
            'humidity'     : float(values[2]),
            'acceleration' : float(values[3] + values[4]),
            'hits'         : int(values[0]),
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
            'acceleration' : float(values[0]),
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
        sys.argv = ['', kwargs.get('port')]
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
            'player'       : int(message['id']),
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
            'player'       : int(message['id']),
            'type'         :'reading',
            'temperature'  : uniform(97, 100), # the arduino doesn't have this
            'humidity'     : uniform(97, 100), # the arduino doesn't have this
            'acceleration' : float(message['accel']),
            'hits'         : int(message['hits']),
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
        self.client.flushInput() # clear backed up data
        return self

    def __parse(self, packet):
        ''' A helper method to parse the packet

        :param packet: The packet to decode
        :returns: The decoded packet
        '''
        result  = None
        packet = packet.replace('\r\n', '')
        message = dict(p.split(':') for p in packet.split(','))
        message_type = message.get('type', None)

        try:
            #_logger.debug("device message: " + packet)
            if message_type == ArduinoTraumaMessage.Type:
                result = ArduinoTraumaMessage.decode(message)
            elif message_type == ArduinoHistoryMessage.Type:
                result = ArduinoHistoryMessage.decode(message)
        except Exception: pass #blah for now
        return result

    def close(self):
        ''' Close the underlying watcher handle
        '''
        self.client.close()

    def next(self):
        ''' Returns the next value from the iterator
       
       :returns: The next value of the iterator 
        '''
        packet = self.client.readline() # technically doesn't read a line...
        return self.__parse(packet)
        

# ----------------------------------------------------------------------------- 
# Main Runner
# ----------------------------------------------------------------------------- 
class DeviceWatcher(object):
    
    def __init__(self, port=None, watcher='arduino'):
        ''' Initialize a new instance of the class
        '''
        self.ipc_queue  = Queue()
        self.halt_event = Event()
        arguments = (self.halt_event, self.ipc_queue, port, watcher)
        self.process = Process(target=self.__watcher, args=arguments)
        self.process.daemon = True

    def start(self):
        ''' Start the processor running

        :returns: The intermessage queue to read from
        '''
        _logger.info("starting the device monitor")
        self.halt_event.clear()
        self.process.start()
        return self.ipc_queue

    def stop(self):
        ''' Stop the processor from running
        '''
        _logger.info("stopping the device monitor")
        self.halt_event.set()
        self.process.join(5)
        if self.process.is_alive():
            _logger.info("force stopping the device monitor")
            self.process.terminate()

    @classmethod
    def __watcher(cls, halt_event, ipc_queue, port, watcher):
        ''' The main runner for pulling messages off the serial
            bus and throwing them into the database
        '''
        if watcher == 'arduino':
            client = ArduinoWatcher(port=port, baudrate=9600, timeout=5)
        else: client = TinyosWatcher(port)
        _logger.info("device monitor initialized")

        try: 
            for message in client:
                if halt_event.is_set():
                    _logger.info("device monitor was told to stop")
                    break # someone told us to stop
                if message: ipc_queue.put(message)
        except Exception:
            _logger.exception("something bad happend in the device monitor")
            ipc_queue.put(None) # we are broke, force an exit
        client.close()
        _logger.info("device monitor exiting")


# ----------------------------------------------------------------------------- 
# Exported Types
# ----------------------------------------------------------------------------- 
__all__ = ['DeviceWatcher']

# ----------------------------------------------------------------------------- 
# Test Runner
# ----------------------------------------------------------------------------- 
if __name__ == "__main__":
    watcher = DeviceWatcher()

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

