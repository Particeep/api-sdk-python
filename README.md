# Particeep API client for Python

Python client-side auth and query the Particeep API

## Obtaining your API access

You can sign up for a Particeep account at https://admin.particeep.com

Please see the [Particeep API docs](https://www.particeep.com/en/doc) for the most up-to-date documentation.


## Requirements

Python 3 or later.

## Usage
```
python3 particeep_api_client.py /path/to/api/endpoint
```

Exemples:
  - `python3 particeep_api_client.py "info"`
  - `python3 particeep_api_client.py "fundraises/search"`
  - `python3 particeep_api_client.py "user/search/dupont"`

## Test

You can run particeep_api_client.py directly in command line like above

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

## Functionalities
  - generate auth secret from key
  - simple querying of all GET API endpoints
  - json return values

#### In progress
  - other REST methods: ie PUT a new user
  - config file
  - higher-level objects
