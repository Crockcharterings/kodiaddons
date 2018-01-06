import os
GLOBAL_PATH = os.path.dirname(os.path.abspath(__file__))
LOG_LEVEL = 'INFO'
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
LOG_FILE = GLOBAL_PATH + '/tvserver.log'
TVSERVER_HOST = '192.168.0.15'
TVSERVER_PORT = '8081'
ACESTREAM_HOST = '192.168.0.15'
ACESTREAM_PORT = '6878'
