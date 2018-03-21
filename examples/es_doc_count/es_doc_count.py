from anchorage.check import Check
import requests
from datetime import datetime


indexname = "*-{}".format(datetime.now().strftime("%Y.%m.%d"))
URL = "http://elastic/{}/_count".format(indexname)


def get_docs(hostname):
    payload = {"query": {"term": {"it_collector": "{}".format(hostname)}}}
    rs = requests.get(URL, json=payload)
    if rs.status_code == 200:
        rsdict = rs.json()
        return rsdict['count']


def check_docs():
    check_results = []
    aggregators = ["nyc_collector", "denver_collector", "london_collector"]
    for host in aggregators:
        res_hash = {}
        res_hash['value'] = get_docs(host)
        res_hash['tags'] = {'host': host}
        check_results.append(res_hash)
    return check_results


check_hash = {
    'it.ls.documents': {
        'rate': 'counter',
        'unit': 'documents',
        'desc': 'the number of documents, per IT collector, pushed into logstash',
        'func': check_docs
    }
}

c = Check(check_hash)


def initialize(url, token):
    c.set_url(url, token)


def execute():
    return c.run_checks()


def run_tests():
    return c.run_tests()
