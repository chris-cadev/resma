import click
import importlib

from click_aliases import ClickAliasedGroup

from resma.ingest.cli import main as main_ingest
from resma.annotate.cli import main as main_annotate
from resma.publish.cli import main as main_publish


@click.group(cls=ClickAliasedGroup)
@click.version_option(version=importlib.metadata.version('resma'), prog_name='resma: Range Signal Meta Amplifier')
def main():
    print('hello world')


commands = {
    'ingest': main_ingest,  # bibliography
    'annotate': main_annotate,  # notes new
    'publish': main_publish,  # gather scatter
}


for name in commands.keys():
    main.add_command(commands.get(name), name)
if __name__ == '__main__':
    main()
