import requests


class Requester:
    def __init__(self, url):
        self.url = url

    def get(self, params=None):
        return requests.get(self.url, params=params)
