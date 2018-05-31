#! /usr/bin/env python3
"""
Requêtes simples sur l'API Particeep
"""

from requests   import get, post, put
from datetime   import datetime
from hashlib    import sha1
from base64     import urlsafe_b64encode
import hmac
from json       import dumps, loads
from sys        import argv, stderr
from os          import path
from configparser import ConfigParser

DEFAULT_CONF = {
    "url": { "scheme": "https:", "server": "api.particeep.com/v1" },
    "consumer": { "key": None  , "sec": None }
}

def read_config():
    """
    Connection parameters: default values and values from ./keys.conf
    """
    conf = DEFAULT_CONF
    parser = ConfigParser()
    parser.read(path.join(".", "keys.conf"))

    for section in conf:
        for k in conf[section]:
            try:
                conf[section][k] = parser[section][k]
            except:
                pass

    return conf


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

def api_request(method, route, payload=None, filepath=None, conf=DEFAULT_CONF):
    """
    endpoint + query [+ payload] => response json
    """
    if route[0] == "/":
        route = route[1:]

    url = conf["url"]["scheme"] + "//" + conf["url"]["server"] + '/' + route

    # logging on stderr
    warn(method + " URL " + url)

    h_date_time = build_date_header()
    h_auth = build_authorization_header(conf["consumer"]["key"], conf["consumer"]["sec"], h_date_time)
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
    elif (method == "POSTnFILE"):
        warn("POST with file and payload:/%s/" % payload)
        fic = open(filepath, "rb")
        resp = post(url, json=loads(payload), headers=headers, files={filepath: fic})
        close(fic)
    elif (method == "PUT"):
        warn("PUT with payload:/%s/" % payload)
        resp = put(url, json=loads(payload), headers=headers)
    if (not hasattr(resp, "status_code")):
        warn("response without status code:", resp)
    if resp.status_code != 200:
        warn("response.status_code", resp.status_code)

    # guess output mode
    mode = "json"
    if route.find("download") != -1:
        mode = "bytes"

    # printing json to STDOUT (or bytes to ./output_binary)
    return handle_response(resp, mode)

def handle_response(resp, mode):
    if mode != "bytes":
        try:
            shown = dumps(resp.json(), indent=2)
        except:
            warn("response wasn't json")
            shown = resp.text
        return shown
    else:
        warn("handling binary response")
        with open("output_binary", 'wb') as fd:
            for chunk in resp.iter_content(chunk_size=128):
                fd.write(chunk)
        return "written to output_binary file"

def warn(*args):
    print(*args, file=stderr)


if __name__ == "__main__":

    conf = read_config()

    if len(argv) == 1:
        warn("DEMO: 'user/name/dupont':")
        shown_resp = api_request("GET", "user/name/dupont", conf=conf)
    elif len(argv) == 2:
        # default method is get
        shown_resp = api_request("GET", argv[1], conf=conf)
    else:
        # exemple args  argv[1]       argv[2]     argv[3]              argv[4]
        #                GET       my/endpoint
        #                PUT       my/endpoint   '{"truc":"bidule"}'
        #                POST      my/endpoint   '{"truc":"bidule"}'
        #             POSTnFILE    my/endpoint   '{"truc":"bidule"}'  /file/to/upload
        shown_resp = api_request(*argv[1:4], conf=conf)

    print(shown_resp)
