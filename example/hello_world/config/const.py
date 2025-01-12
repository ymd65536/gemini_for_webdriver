import os
PORT = os.getenv('WEBDRIVER_PORT', None)
WEB_DRIVER_URL = 'http://localhost:{0}/session'.format(PORT)
