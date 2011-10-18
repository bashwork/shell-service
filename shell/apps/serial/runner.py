from twisted.internet import reactor, task
from twisted.web.server import Site
from twisted.web import server
from twisted.web.resource import Resource
from shell.apps.api.models import Player
from random import randint, random

class StreamingPage(Resource):
    isLeaf = True

    def __init__(self):
        self.presence=[]
        loopingCall = task.LoopingCall(self.__new_reading)
        loopingCall.start(1, False)
        Resource.__init__(self)

    def render_GET(self, request):
        print "new client", request
        request.write('OK')
        self.presence.append(request)
        return server.NOT_DONE_YET
    
    def __new_reading(self):
        parameters = (randint(0,4), randint(0,100),
            random()*100, random()*100, random()*100)
        reading = '{"player":%d, "hits":%d, "temperature":%f, "humidity":%f, "acceleration":%f}' % parameters

        for client in self.presence:
            client.write(reading)

def start_server(port=8080):
    print "Starting Streaming Service [%s]" % port
    resource = StreamingPage()
    factory = Site(resource)
    reactor.listenTCP(port, factory)
    reactor.run()

