from anchorage.main import main
from click.testing import CliRunner
import json


def test_main():
    '''This will always fail, please make your tests work!'''
    runner = CliRunner()
    result = runner.invoke(main, ['testmodule', 'http://foo',  '--test'])
    parsed_json = json.loads(result.output)
    assert isinstance(parsed_json, dict)
