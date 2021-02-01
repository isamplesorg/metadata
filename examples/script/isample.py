"""
Python script to retrieve sample metadata examples.

Note - there are many shortcuts in here, not to be used
as a general purpose mechanism for accessing these collections.
"""

import logging
import json
import requests
import click
import common

LOG_LEVELS = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "WARN": logging.WARNING,
    "ERROR": logging.ERROR,
    "FATAL": logging.CRITICAL,
    "CRITICAL": logging.CRITICAL,
}
LOG_DATE_FORMAT = "%Y-%m-%dT%H:%M:%S"
LOG_FORMAT = "%(asctime)s %(name)s:%(levelname)s: %(message)s"
DEFAULT_ACCEPT = "application/json"
DEFAULT_HEADERS = {"Accept": DEFAULT_ACCEPT, "User-Agent": "isampler-0.1/python-3"}
REQUEST_OPTIONS = {
    "timeout": 30,
    "allow_redirects": True
}


def getLogger():
    return logging.getLogger("isampler")

def logResponse(response):
    L = getLogger()
    for r in response.history:
        L.info(f"url: {r.url}")
        L.info(f"status: {r.status_code}")
        L.info(f"content-type: {r.headers.get('Content-Type', '-')}")
        L.info(f"link: {r.headers.get('Link', '-')}")
        L.info("----")
    r = response
    L.info(f"url: {r.url}")
    L.info(f"status: {r.status_code}")
    L.info(f"content-type: {r.headers.get('Content-Type', '-')}")
    L.info(f"link: {r.headers.get('Link', '-')}")
    L.info("----")



def getSmithsonianFishRecord(identifier, accept=DEFAULT_ACCEPT):
    """
    Get a record from the Smithsonian fishes collection.

    This is a hack to access a record from the Smithsonian fishes
    collection. The service is likely to change without notice.

    Args:
        identifier: ARK identifier for the specimen record

    Returns:
        dict representation of the record

    """
    L = getLogger()
    identifier = identifier.lower().strip()
    assert identifier.startswith("ark:")
    hacked_ark = identifier.split("/")[2]
    hacked_ark = hacked_ark[1:].replace("-", "")
    url = "https://collections.nmnh.si.edu/search/fishes/search.php"
    params = {
        "action": 1,
        "qtype": 12,
        "view": "keyword:gallery",
        "start": 0,
        "sort": "idefa.ideqn",
        "cart": "false",
        "dir": "ASC",
        "terms": "ark " + hacked_ark,
    }
    headers = DEFAULT_HEADERS
    headers["Accept"] = accept
    response = requests.get(url, params=params, headers=headers, **REQUEST_OPTIONS)
    logResponse(response)
    assert response.status_code == 200
    data = json.loads(response.text)
    return data


def getSESARRecord(identifier, accept=DEFAULT_ACCEPT):
    """

    Args:
        identifier:

    Returns:

    """
    L = getLogger()
    identifier = identifier.upper()
    if identifier.startswith("igsn:"):
        identifier = identifier[len("IGSN:"):]
    url = f"https://app.geosamples.org/sample/igsn/{identifier}"
    headers = DEFAULT_HEADERS
    headers["Accept"] = accept
    response = requests.get(url, headers=headers, **REQUEST_OPTIONS)
    logResponse(response)
    assert response.status_code == 200
    data = json.loads(response.text)
    return data


def getGEOMERecord(identifier, accept=DEFAULT_ACCEPT):
    """

    Args:
        identifier:

    Returns:

    """
    #LOL - do not encode path parameter for GEOME
    url = f"https://api.geome-db.org/records/{identifier}"
    params = {
        "includeParent":1,
        "includeChildren":1,
    }
    headers = DEFAULT_HEADERS
    headers["Accept"] = accept
    response = requests.get(url, headers=headers, params=params, **REQUEST_OPTIONS)
    logResponse(response)
    assert response.status_code == 200
    data = json.loads(response.text)
    return data


def getOpenContextRecord(identifier, accept=DEFAULT_ACCEPT):
    """
    ark%3A%2F28722%2Fk27w68z78
    Args:
        identifier:

    Returns:

    """
    url = "https://opencontext.org/subjects-search/"
    params = {
        "id":identifier
    }
    headers = DEFAULT_HEADERS
    headers["Accept"] = accept
    response = requests.get(url, headers=headers, params=params, **REQUEST_OPTIONS)
    logResponse(response)
    assert response.status_code == 200
    data = json.loads(response.text)
    return data


@click.command()
@click.option(
    "-v",
    "--verbosity",
    default="WARNING",
    help="Specify logging level",
    show_default=True,
)
@click.option(
    "-a",
    "--accept",
    default=DEFAULT_ACCEPT,
    help="Accept header value",
    show_default=True,
)
@click.option(
    "-c",
    "--collection",
    default="smithsonian",
    help="Which collection to access",
    show_default=True,
)
@click.argument("identifier")
def main(verbosity, accept, collection, identifier):
    common.setupLogging(verbosity)
    collection = collection.lower()
    data = {}
    if collection.find("smith") >= 0:
        data = getSmithsonianFishRecord(identifier, accept=accept)
    elif collection.find("ses") >= 0:
        data = getSESARRecord(identifier, accept=accept)
    elif collection.find("geom") >= 0:
        data = getGEOMERecord(identifier, accept=accept)
    elif collection.find("open") >= 0:
        data = getOpenContextRecord(identifier, accept=accept)
    else:
        L.error("Don't know the collection %s", collection)
        return
    print(json.dumps(data, indent=2))


if __name__ == "__main__":
    main(obj={})
