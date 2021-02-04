import requests
from requests.exceptions import HTTPError
import urllib.request as urllib2



class HttpHelpers:
    def __init__(self):
        self.session = requests.Session()

    def download_page(self, url):

        try:
            req = urllib2.Request(url)
            response = urllib2.urlopen(req,timeout=100000) 
            html = response.read().decode('utf-8')
        except HTTPError as httpErr:
            print(f'Http error occurred: {httpErr}')
            return None
        except Exception as err:
            print(f'A generic error occurred: {err}')
            return None
        else:
            return html