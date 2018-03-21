anchorage
===============
Anchorage is a small python framework for emitting metadata-defined metrics into Bosun.


- Create a new python file with the below contents.  
- Define your metrics in check_hash
- write your actual check logic in the func defined in check_hash, in the below example testcheck()
- your check function must return a hash with value defined by 'value' key, and a sub-hash of tags in key 'tags'.

Example instantiation: `anchorage --debug --test --token <bosun-auth-token> <modulename-not-filename> <url-of-bosun-server>`

- --test does not send data to the server.
- --debug enables debug logging inside of anchorage


To execute the testmodule example, use `anchorage --debug --test testmodule http://invalidurl`

Example of testmodule:
```
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
```
