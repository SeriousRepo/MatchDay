from app.constants import MATCHDAY_SERVER_KEY, MATCHDAY_BASE_URL
import json
import requests


class Connector:
    __base_url = MATCHDAY_BASE_URL
    __headers = {'content-type': 'application/json',
                 'authorization': 'Token {}'.format(MATCHDAY_SERVER_KEY)}

    def send_post(self, content, url_sufix):
        json_content = json.dumps(content)
        response = requests.request("POST", self.__base_url + url_sufix, data=json_content, headers=self.__headers)

        if response.status_code != 201:
            print(response.text)
            response.raise_for_status()

        return response.content

    def send_put(self, content, url_sufix):
        json_content = json.dumps(content)
        response = requests.request('PUT', self.__base_url + url_sufix, data=json_content, headers=self.__headers)

        if response.status_code != 200:
            print(response.text)
            response.raise_for_status()

        return response.content

    def send_get(self, url_sufix):
        response = requests.request('GET', self.__base_url + url_sufix, headers=self.__headers)

        if response.status_code != 200:
            print(response.text)
            response.raise_for_status()

        return response.content

    def send_delete(self, url_sufix):
        response = requests.request('DELETE', self.__base_url + url_sufix, headers=self.__headers)

        if response.status_code != 204:
            print(response.text)
            response.raise_for_status()

        return response.content
