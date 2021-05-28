import pytest
import json
import requests

url = "https://mars.cyverse.org/thing/?offset={0}&limit=1000&status=200&authority=SESAR"
thing_url = "https://mars.cyverse.org/thing/{0}?full=false"


def pytest_report_header(config):
    return "Going to fetch records from cyverse"


offset_values = [0, 1001]


def get_record(id):
    response = requests.get(thing_url.format(id))
    json = response.json()
    return json


@pytest.mark.parametrize("offset", offset_values)
def test_pull_down_records(offset):
    response = requests.get(url.format(offset))
    json = response.json()
    data = json["data"]
    records = [get_record(record["id"]) for record in data]
    print("\n\nRecords are " % records)
