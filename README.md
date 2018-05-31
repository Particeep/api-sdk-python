# Particeep API client for Python

Python client-side auth and query the Particeep API


## Obtaining your API access

You can sign up for a Particeep account at https://admin.particeep.com

Please see the [Particeep API docs](https://www.particeep.com/en/doc) for the most up-to-date documentation.


## Functionalities
  - command line querying of all Particeep API endpoints
  - generate auth secret from key/secret in `keys.conf`
  - output return values:
    - binary file for download endpoints
    - json for all the other endpoints


## Requirements

Python 3 or later.


## Usage

You can run particeep_api_client.py directly in command line

```
python3 particeep_api_client.py /path/to/api/endpoint
python3 particeep_api_client.py METHOD /path/to/api/endpoint
python3 particeep_api_client.py METHOD /path/to/api/endpoint '{jsonpayload}'
python3 particeep_api_client.py METHOD /path/to/api/endpoint '{jsonpayload}' > output.json
```

Exemples:
  - `python3 particeep_api_client.py info`
  - `python3 particeep_api_client.py fundraises/search`
  - `python3 particeep_api_client.py user/search/dupont"`
  - `python3 particeep_api_client.py PUT form/answer/<user_id> '[{"question_id":"<question_id>","answer":["Yes"]}]'`
  - `python3 particeep_api_client.py POST loan/fundraise/<fundraise_id> '{"amount_target": 500000}'`


## Config
The file `keys.conf` contains the values that will be used:
  - to build the url of the API server to query (section `[url]`)
      - exemple:
        ```
        scheme = http:
        server = local.particeep.com:9100/v1
        ```

  - as authentication keys (section `[consumer]`)
      - exemple:
        ```
        key = test_flow_928c5516-e56e-4dd3-9ffb-5
        sec = 12345678-0000-1000-a000-0123456789ab
        ```
      - to get your keys, see *Obtaining your API access* above

Values should not be quoted. Any key can be commented out with '#'


## Importing as a lib

You can also import functions from particeep_api_client.py like this:
```
from particeep_api_client import build_authorization_header, build_date_header
```

Then, a full test module could look like this:

```
from particeep_api_client import build_authorization_header, build_date_header
import requests

def test():
    url = "http://api.particeep.com/v1/info"
    api_key = "d6a53e1a-fc8e-4251-9dda-fabbce5f2a2c"
    api_secret = "9bb3c122-0272-4bed-a632-19d5d52c7b5e"
    date_time = build_date_header()
    headers={
        "Authorization": build_authorization_header(api_key, api_secret, date_time),
        "DateTime": date_time,
        "Accept": "application/json"
    }
    http_response = requests.get(url, headers=headers)
    print("status: %i" % http_response.status_code)
    print("json: %s" % http_response.json())
```

(c) 2017-2018 Particeep
