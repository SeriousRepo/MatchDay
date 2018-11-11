import os

try:
    MATCHDAY_SERVER_KEY = os.environ.get('MATCHDAY_SERVER_KEY')
except KeyError:
    error_msg = "cannot find environment variable"
    raise KeyError(error_msg)


MATCHDAY_BASE_URL = 'https://matchday-server.herokuapp.com/'
