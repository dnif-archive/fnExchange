import os
from os import environ

import click
import sys

from fnexchange.core.plugins import PluginBuilder, PluginConfig
from fnexchange.core.config import read_config
from fnexchange.server.app import start_app
from fnexchange.server.handlers import APIHandler


@click.group()
@click.pass_context
def cli(ctx):
    pass


def __print_configtest_error(message):
    click.echo('')
    click.echo("# ERROR: {0}".format(message), err=True)
    click.echo('')


def __print_configtest_outcome(valid):
    error = not valid
    click.echo('')
    click.echo("#" * 30, err=error)
    click.echo("# Validation {0} !".format('Succeeded' if valid else 'Failed'), err=error)
    click.echo("#" * 30, err=error)


@cli.command()
@click.option('--conf', required=True)
@click.pass_context
def configtest(ctx, conf):
    """Validate the fnexchange conf file"""
    click.echo("Validating configuration file")
    valid = True

    try:
        config = read_config(conf)
    except Exception, e:
        __print_configtest_error(str(e))
        __print_configtest_outcome(False)
        return

    click.echo("Configuration file loaded successfully.")

    # validate server config
    click.echo("Validating conf.server configuration.")
    server_config = config['conf']['server']
    if server_config.get('auth_required') and not server_config.get('auth_tokens'):
        __print_configtest_error("'auth_tokens' is mandatory if 'auth_required' is True")
        valid = False

    # validate plugins_enabled
    click.echo(os.linesep + "Validating conf.plugins_enabled configuration.")
    plugins_conf = config['conf']['plugins_enabled']
    for alias, params_dict in plugins_conf.items():
        try:
            class_name = None
            class_name = params_dict['class_name']
            plugin_config = PluginConfig(**(params_dict.get('config') or {}))
            PluginBuilder.build_plugin(class_name=class_name, config=plugin_config)
            click.echo("  - alias '{0}' : plugin '{1}' initialized successfully".format(alias, class_name))
        except Exception, e:
            click.echo("  - alias '{0}' : plugin '{1}' initialization failed".format(alias, class_name), err=True)
            __print_configtest_error(str(e))
            # traceback.print_exc()
            valid = False

    __print_configtest_outcome(valid)


def __create_handler_settings(config):
    """ :type config: dict """
    server_config = config['conf']['server']
    plugins_conf = config['conf']['plugins_enabled']

    api_handler_settings = {
        'auth_required': server_config.get('auth_required', True),
        'upstream_timeout': server_config.get('upstream_timeout', None),
        'registry': PluginBuilder.build_plugins(plugins_conf),
    }
    if api_handler_settings['auth_required']:
        api_handler_settings['auth_tokens'] = server_config['auth_tokens']

    return {
        APIHandler: api_handler_settings
    }


@cli.command()
@click.option('--conf', required=True)
@click.option('--port', default=None)
@click.option('--foreground/--background', is_flag=True, default=True)
@click.pass_context
def runserver(ctx, conf, port, foreground):
    """Run the fnExchange server"""
    config = read_config(conf)

    debug = config['conf'].get('debug', False)
    click.echo('Debug mode {0}.'.format('on' if debug else 'off'))

    port = port or config['conf']['server']['port']

    app_settings = {
        'debug': debug,
        'auto_reload': config['conf']['server'].get('auto_reload', False),
    }
    handlers_settings = __create_handler_settings(config)

    if foreground:
        click.echo('Requested mode: foreground')
        start_app(port, app_settings, handlers_settings)
    else:
        click.echo('Requested mode: background')
        # subprocess.call([sys.executable, 'yourscript.py'], env=os.environ.copy())
        raise NotImplementedError


if __name__ == '__main__':
    cli(sys.argv[1:])
