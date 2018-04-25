import click
from box_archive import __version__
from box_access import BoxAccess

# Globals
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


# Helper callbacks
def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo('BoxArchive {}'.format(__version__))
    ctx.exit()


@click.group(context_settings=CONTEXT_SETTINGS)
@click.option('-V', '--version', is_flag=True, callback=print_version, expose_value=False, is_eager=True,
              help='Print the current version number and exit.')
def main():
    """BoxArchive lets you archive files and folders on your system to your Box account"""
    click.echo(click.get_current_context().get_help())
