import requests


def connect(uri):
    credentials = {'X-Auth-Token': 'bb90e5856e754ff5a1be11d9640d5ff2'}
    response = requests.get(uri, headers=credentials)
    if response.status_code is 200:
        return response.content
    else:
        response.raise_for_status()
