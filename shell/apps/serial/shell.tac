'''
run with: twistd -ny shell.tac
'''
import logging, sys
from twisted.python import log
from twisted.web import server
from twisted.web.wsgi import WSGIResource
from twisted.python.threadpool import ThreadPool
from twisted.internet import reactor
from twisted.application import service, strports
import service as Shell

# ----------------------------------------------------------------------------- 
# get our configuration
# ----------------------------------------------------------------------------- 
try:
    from local_settings import *
except ImportError:
    print "No configuration settings file found"
    sys.exit(1)

# ------------------------------------------------------------
# enable twisted logging and python logging
# ------------------------------------------------------------
logging.basicConfig()

logger = logging.getLogger()
logger.setLevel(LOGGING_LEVEL)

#observer = log.PythonLoggingObserver()
#observer.start()

# ------------------------------------------------------------
# create and start a thread pool,
# ------------------------------------------------------------
wsgiThreadPool = ThreadPool()
wsgiThreadPool.start()

# ------------------------------------------------------------
# start the processing service
# ------------------------------------------------------------
processor = None # for scopes sake
try:
    processor = Shell.ShellProcessor(service_base=SERVICE_BASE,
        device_port=DEVICE_PORT, device_type=DEVICE_TYPE,
        twilio_account=TWILIO_ACCOUNT, twilio_token=TWILIO_TOKEN)
    processor.start()
except Exception as ex:
    logger.exception("System failed to start")

# ------------------------------------------------------------
# ensuring that it will be stopped when the reactor shuts down
# ------------------------------------------------------------
def twisted_shutdown():
    logger.info('twisted shutdown callback called')
    wsgiThreadPool.stop()
    if processor != None:
        processor.stop()
        processor.join(5)
    logger.info('twisted shutdown callback finished')

reactor.addSystemEventTrigger('after', 'shutdown', twisted_shutdown)

# ------------------------------------------------------------
# create the WSGI resource
# ------------------------------------------------------------
wsgiAppAsResource = WSGIResource(reactor, wsgiThreadPool, Shell.main)
application = service.Application('Shell Streaming Service')
server = strports.service(STREAMING_PORT, server.Site(wsgiAppAsResource))
server.setServiceParent(application)
