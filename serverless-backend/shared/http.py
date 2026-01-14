import requests

DEFAULT_TIMEOUT = (3.05, 10)  # connect, read


def post(url: str, *, headers=None, data=None, json=None, timeout=DEFAULT_TIMEOUT):
    return requests.post(url, headers=headers, data=data, json=json, timeout=timeout)


def get(url: str, *, headers=None, params=None, timeout=DEFAULT_TIMEOUT):
    return requests.get(url, headers=headers, params=params, timeout=timeout)
