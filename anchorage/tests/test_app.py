from anchorage.main import main
from click.testing import CliRunner
import json


def test_main():
    '''end-to-end execution test in test mode'''
    runner = CliRunner()
    result = runner.invoke(main, ['example', 'http://foo',  '--test'])
    parsed_json = json.loads(result.output)
    assert isinstance(parsed_json, dict)
