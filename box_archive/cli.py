import logging

import click
import click_log

from box_archive import __version__
from box_archive.helpers import constants
from box_archive.helpers.box_access import BoxAccess

# Globals

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
logger = logging.getLogger(__name__)
click_log.basic_config(logger)


# Helper callbacks
def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo('BoxArchive {}'.format(__version__))
    ctx.exit()


@click.group(context_settings=CONTEXT_SETTINGS)
@click.option('-V', '--version', is_flag=True, callback=print_version, expose_value=False, is_eager=True,
              help='Print the current version number and exit.')
@click_log.simple_verbosity_option(logger)
@click.option('-d', '--debug', is_flag=True, default=False)
def main(debug):
    """BoxArchive lets you archive files and folders on your system to your Box account"""
    if debug:
        logger.setLevel(logging.DEBUG)
        pass
    else:
        logger.setLevel(logging.INFO)
        pass
    click.secho(constants.welcome_text, fg='green')
    pass


@main.command()
def init():
    """Logs in to Box, initializes CLI, and stores auth token"""
    logger.info("Logging in to Box now")
    boxAccess = BoxAccess.instance()
    if not boxAccess.logged_in:
        boxAccess.login_prompt()

    # Authenticated now
    try:
        click.secho("\n\n***** Logged in as: {0} *****".format(boxAccess.get_user()['login']), fg='green')
    except RuntimeError as e:
        print(e)
    pass
