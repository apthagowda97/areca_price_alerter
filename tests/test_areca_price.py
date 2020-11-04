import requests
import os

def test_requests_status():
    assert requests.get(open('url.txt').read()).status_code == 200