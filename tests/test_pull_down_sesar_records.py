import concurrent
import random
import json
import requests
import requests.sessions

dir = "/Users/mandeld/iSamples/tmprecords/{0}.json"
url = "https://mars.cyverse.org/thing/?offset={0}&limit={1}&status=200&authority=SESAR"
thing_url = "https://mars.cyverse.org/thing/{0}?full=false"
BATCH_SIZE = 100
DEFAULT_THREAD_COUNT = 10


def pytest_report_header(config):
    return "Going to fetch records from cyverse"


def get_record(s, id):
    print("Fetching record with id " + id)
    response = s.get(thing_url.format(id))
    json_response = response.json()
    with open(dir.format(id), "w") as outfile:
        json.dump(json_response, outfile)
    return json_response


def test_pull_down_records():
    with requests.Session() as s:
        # pull down a random sampling of 100 records somewhere between 0 and total_records - 100
        response = s.get(url.format("0", "1"))
        json = response.json()
        total_records = json["total_records"]
        offset = random.randint(0, total_records - BATCH_SIZE)
        url_to_check = url.format(offset, BATCH_SIZE)
        print("Pulling data down from url " + url_to_check)
        response = s.get(url_to_check)
        json = response.json()
        data = json["data"]

        for record in data:
            get_record(s, record["id"])

    # Some of the data wasn't getting written to disk with this approach:
    # with concurrent.futures.ThreadPoolExecutor(
    #         max_workers=DEFAULT_THREAD_COUNT
    # ) as executor:
    #     futures = []
    #     for record in data:
    #         futures.append(executor.submit(get_record, record["id"]))
