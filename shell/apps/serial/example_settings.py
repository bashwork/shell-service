# ------------------------------------------------------------
# service configuration
# ------------------------------------------------------------
import logging
LOGGING_LEVEL  = logging.DEBUG
STREAMING_PORT = 'tcp:8080'

# ------------------------------------------------------------
# twilio configuration
# ------------------------------------------------------------
TWILIO_ACCOUNT = 'your twilio account identifier'
TWILIO_TOKEN   = 'your twilio account token'

# ------------------------------------------------------------
# streaming device configuration
# ------------------------------------------------------------
DEVICE_TYPE    = "arduino"
DEVICE_PORT    = "/dev/ttyUSB0"

#DEVICE_TYPE   = "tinyos"
#DEVICE_PORT   = "serial@/dev/ttyUSB0:57600"

# ------------------------------------------------------------
# service client configuration
# ------------------------------------------------------------
SERVICE_BASE   = 'http://localhost:8000/api/v1/'
