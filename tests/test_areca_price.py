import requests
import os

def test_requests_status():
    assert requests.get(open('url.txt').read(), verify=False).status_code == 200
