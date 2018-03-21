import click
import importlib
import logging
import sys


def init_log(debug):
    if debug:
        loglevel = logging.DEBUG
    else:
        loglevel = logging.WARN
    logformat = '%(asctime)s:%(levelname)s:%(name)s:%(message)s'
    logging.basicConfig(format=logformat, level=loglevel)


@click.command()
@click.argument('module', envvar='ANCHORAGE_MODULE')
@click.argument('url', envvar='ANCHORAGE_BOSUN_URL')
@click.option('--token', default=None, envvar='ANCHORAGE_BOSUN_TOKEN')
@click.option('--debug/--no-debug', default=False)
@click.option('--test/--no-test', default=False)
def main(module, url, token, debug, test):
    init_log(debug)
    sys.path.append('.')

#    try:
    plugin = importlib.import_module(module)
#    except Exception as e:
#        logging.error("Module not found.  Be sure to use module name and not filename.  e:{}".format(e))
#        sys.exit(255)

    try:
        plugin.initialize(url, token)
    except Exception as e:
        logging.error("Plugin does not contain an initialize method, which is required.  e:{}".format(e))
        sys.exit(254)

    if test:
        try:
            print(plugin.run_tests())
        except AttributeError as e:
            logging.error("Error emitted from test run. Is run_tests() defined in your plugin?  e: {}".format(e))
            sys.exit(253)

    else:
        plugin.execute()


if __name__ == '__main__':
    main()
