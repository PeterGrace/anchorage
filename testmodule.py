from anchorage.check import Check


def testcheck():
    return {
        'value': '0',
        'tags':
            {'host': 'host'}
    }

check_hash = {
    'pete.widgets': {
        'rate': 'gauge',
        'unit': 'Widgets per Fortnight',
        'desc': 'the number of widgets created per fortnight of production',
        'func': testcheck
    }
}

c = Check(check_hash)


def initialize(url, token):
    c.set_url(url, token)


def execute():
    return c.run_checks()


def run_tests():
    return c.run_tests()
