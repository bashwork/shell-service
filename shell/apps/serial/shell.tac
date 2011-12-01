'''
run with: twistd -ny shell.tac
'''
import logging
from twisted.python import log
from twisted.web import server
from twisted.web.wsgi import WSGIResource
from twisted.python.threadpool import ThreadPool
from twisted.internet import reactor
from twisted.application import service, strports
import service as Shell

# ------------------------------------------------------------
# enable twisted logging and python logging
# ------------------------------------------------------------
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
observer = log.PythonLoggingObserver()
observer.start()

# ------------------------------------------------------------
# create and start a thread pool,
# ------------------------------------------------------------
wsgiThreadPool = ThreadPool()
wsgiThreadPool.start()

# ------------------------------------------------------------
# start the processing service
# ------------------------------------------------------------
processor = Shell.ShellProcessor()
processor.start()

# ------------------------------------------------------------
# ensuring that it will be stopped when the reactor shuts down
# ------------------------------------------------------------
def twisted_shutdown():
    wsgiThreadPool.stop()
    processor.stop()

reactor.addSystemEventTrigger('after', 'shutdown', twisted_shutdown)

# ------------------------------------------------------------
# Create the WSGI resource
# ------------------------------------------------------------
wsgiAppAsResource = WSGIResource(reactor, wsgiThreadPool, Shell.main)
application = service.Application('Twisted.web.wsgi Hello World Example')
server = strports.service('tcp:8080', server.Site(wsgiAppAsResource))
server.setServiceParent(application)
