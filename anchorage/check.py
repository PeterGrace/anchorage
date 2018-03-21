from datetime import datetime
import logging
import json
from requests import Session


class Check:

    def __init__(self, checktable):
        self.metadata = checktable

    def set_url(self, url, token):
        self.s = Session()
        self.s.headers.update({'X-Access-Token': token})
        self.url = url

    def make_payload(self, objdict):
        if not isinstance(objdict['response'], dict):
            logging.error("Your check must return a dict containing a key for value and a key for array of tags.")
            return None

        ts = int(datetime.now().timestamp())
        rethash = {}
        rethash['metric'] = objdict['metric']
        if 'value' in objdict['response']:
            rethash['value'] = objdict['response']['value']
        else:
            logging.error("Missing check value in return of check function")
            return None
        if 'tags' in objdict['response']:
            if 'host' in objdict['response']['tags']:
                rethash['tags'] = objdict['response']['tags']
            else:
                logging.error("We need a 'host' tag or we cannot pass the metric to bosun.")
                return None
        else:
            logging.error("Missing tags in return of check function.  At the minimum, we require a 'host' tag.")
            return None

        rethash['timestamp'] = ts
        return rethash

    def get_results(self):
        checks = []
        for check in self.metadata.keys():
            response = self.metadata[check]['func']()
            if isinstance(response, list):
                for i in response:
                    checks.append(self.make_payload({"metric": check, "response": i}))
            else:
                checks.append(self.make_payload({"metric": check, "response": response}))
        logging.debug(checks)
        return checks

    def run_checks(self):
        self.send_metadata()
        rs = self.get_results()
        url = "{}/api/put".format(self.url)
        resp = self.s.post(url, json=rs)
        if resp.status_code < 400:
            return True
        else:
            logging.error("Error sending metrics: {}".format(resp.text))

    def run_tests(self):
        yoke = {}
        yoke['metadata'] = self.get_metadata()
        yoke['results'] = self.get_results()
        logging.debug("Yoke is {}".format(yoke))
        return json.dumps(yoke, indent=4)

    def get_metadata(self):
        md = []
        for metric in self.metadata.keys():
            for item in self.metadata[metric].keys():
                if item == "func":
                    continue
                md.append({"metric": metric, "Name": item, "Value": self.metadata[metric][item]})

        logging.debug(md)
        return md

    def send_metadata(self):
        md = self.get_metadata()
        url = "{}/api/metadata/put".format(self.url)
        logging.debug("Sending metadata: {}".format(md))
        resp = self.s.post(url, json=md)
        if resp.status_code < 400:
            return True
        else:
            logging.error("Error sending metadata: {}".format(resp.text))
