import sys
import logging

# Setup the logging facility
logging.basicConfig(stream = sys.stdout, level = logging.DEBUG)
logger = logging.getLogger('chat')