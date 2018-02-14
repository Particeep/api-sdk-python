#! /usr/bin/env python3
"""
Requêtes simples sur l'API Particeep
"""

from requests   import get, post
from datetime   import datetime
from hashlib    import sha1
from base64     import urlsafe_b64encode
import hmac
from json       import dumps, loads
from sys        import argv, stderr

# ROUTE
SCHEME = "https:"
# SRV = "localhost:9100"
SRV = "test-api.particeep.com"
VER = "v1"

# AUTH KEY
KEY = "d6a53e1a-fc8e-4251-9dda-fabbce5f2a2c"
SEC = "9bb3c122-0272-4bed-a632-19d5d52c7b5e"

def build_authorization_header(api_key, api_secret, date_time):
    to_sign = api_secret + api_key + date_time
    msg_bytes = bytes(to_sign, 'utf-8')
    sec_bytes = bytes(api_secret, 'utf-8')
    hasher = hmac.new(sec_bytes, msg_bytes, sha1)
    hex_signature = hasher.hexdigest()
    b64_signature = urlsafe_b64encode(bytes(hex_signature, 'utf-8'))
    return ':'.join(["PTP",api_key,str(b64_signature, 'UTF-8')])

def build_date_header():
    return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

def api_request(method, route, payload=None):
    """
    endpoint + query [+ payload] => response json
    """
    if route[0] == "/":
        route = route[1:]

    url = SCHEME + "//" + SRV + '/' + VER + '/' + route

    warn("URL:" + url)
    h_date_time = build_date_header()
    h_auth = build_authorization_header(KEY, SEC, h_date_time)
    headers={
        "Authorization": h_auth,
        "DateTime": h_date_time,
        "Accept": "application/json"
    }
    resp = None
    if (method == "GET"):
        resp = get(url, headers=headers)
    elif (method == "POST"):
        warn("POST with payload:/%s/" % payload)
        resp = post(url, json=loads(payload), headers=headers)
    if resp.status_code == 200:
        return resp.json()
    else:
        warn("response.status_code", resp.status_code)
        return resp.text


def warn(*args):
    print(*args, file=stderr)


if __name__ == "__main__":
    if len(argv) == 2:
        print("ARGV", argv)
        resp_json = api_request("GET", argv[1])
    elif len(argv) > 2:
        resp_json = api_request("POST", argv[1], argv[2])
    else:
        warn("DEMO: 'user/name/dupont':")
        resp_json = api_request("GET", "user/name/dupont")

    print(dumps(resp_json, indent=2))
