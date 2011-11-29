#!/usr/bin/env python
'''
A simple serial logger for the shell firmware
messages.
'''
import sys, time
import tinyos
from multiprocessing import Process, Queue, Event 


# ----------------------------------------------------------------------------- 
# Classes
# ----------------------------------------------------------------------------- 
class ShellMessage(tinyos.Packet):

    Type = 0x93

    def __init__(self, packet = None):
        ''' Initialize a new instance of the ShellMessage

        :param packet: The packet to parse
        '''
        settings = [
            ('version',  'int', 2),
            ('interval', 'int', 2),
            ('id',       'int', 2),
            ('count',    'int', 2),
            ('readings', 'blob', None)]
        tinyos.Packet.__init__(self, settings, packet)


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
        self.process.start()
        return self.queue

    def stop(self):
        ''' Stop the processor from running
        '''
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
    
        while not event.is_set():
            queue.put("hello world")
            time.sleep(1)
            #packet = messages.read()
            #if packet and (packet.type == ShellMessage.Type):
            #    message = ShellMessage(p.data)
            #    # TODO do some kind of processing
            #    queue.put(message)

# ----------------------------------------------------------------------------- 
# Exported Types
# ----------------------------------------------------------------------------- 
__all__ = ['SerialWatcher']
