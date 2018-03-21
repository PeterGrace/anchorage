from anchorage.check import Check
from wsman import WSMan
from wsman.provider.remote import Remote
from wsman.transport.process import Subprocess
from wsman.format.command import OutputFormatter
from wsman.loghandlers.HTMLHandler import HTMLHandler
from time import time


WS_PATH="root/dell/cmc"
SCHEMA="http://schemas.dell.com/wbem/wscim/1/cim-schema/2"

VRTX_HOSTS = ['vrtx01', 'vrtx02', 'vrtx03']

wsman = WSMan(transport=Subprocess())


def iterate_chassis():
    rs = []
    for vrtx in VRTX_HOSTS:
        rs.append(get_vrtx_chassis(vrtx))

    return rs


def get_vrtx_chassis(name):
    CLASSNAME = "DCIM_ModularChassisView"

    remote = Remote(name, 'root', 'foobar')
    rs = wsman.enumerate(CLASSNAME, WS_PATH, remote=remote, uri_host=SCHEMA)
    logging.debug("rs = {}".format(rs))

    return {
        'value': '0',
        'tags':
            {'host': name}
    }

check_hash = {
    'vrtx.chassis.primary_status': {
        'rate': 'gauge',
        'unit': 'Status Code',
        'desc': 'The status of the VRTX chassis as reported by the chassis itself.',
        'func': iterate_chassis
    }
}

c = Check(check_hash)


def initialize(url, token):
    c.set_url(url, token)

def execute():
    return c.run_checks()


def run_tests():
    return c.run_tests()
