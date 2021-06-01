import pytest
import json
import requests
import requests.sessions

dir = "/Users/mandeld/iSamples/tmprecords/{0}.json"
url = "https://mars.cyverse.org/thing/?offset={0}&limit=1000&status=200&authority=SESAR"
thing_url = "https://mars.cyverse.org/thing/{0}?full=false"


def pytest_report_header(config):
    return "Going to fetch records from cyverse"


offset_values = [0, 1001]


def get_record(s, id):
    response = s.get(thing_url.format(id))
    json_response = response.json()
    with open(dir.format(id), "w") as outfile:
        json.dump(json_response, outfile)
    return json_response


@pytest.mark.parametrize("offset", offset_values)
def test_pull_down_records(offset):
    with requests.Session() as s:
        response = requests.get(url.format(offset))
        json = response.json()
        data = json["data"]
        records = [get_record(s, record["id"]) for record in data]
    print("\n\nRecords are " % records)
