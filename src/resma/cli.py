import importlib
import os
import sys
import traceback

from click import echo, group, pass_context, version_option
from click_aliases import ClickAliasedGroup

from resma.annotate.interfaces.factories.configuration_factory import make_annotate_configuration
from resma.ingest.cli import main as main_ingest
from resma.annotate.cli import main as main_annotate
from resma.publish.cli import main as main_publish


@group(cls=ClickAliasedGroup)
@version_option(version=importlib.metadata.version('resma'), prog_name='resma: Range Signal Meta Amplifier')
@pass_context
def main(ctx):
    pass


commands = {
    'annotate': (main_annotate, ('note', 'n')),  # notes new
    'ingest': (main_ingest, ('ing', 'i')),  # bibliography
    'publish': (main_publish, ('pub', 'p')),  # gather scatter
}


for name in commands.keys():
    cmd, aliases = commands.get(name)
    main.add_command(cmd, name, aliases=aliases)
if __name__ == '__main__':
    dev_mode = os.getenv('RESMA_RUNTIME_MODE') == 'dev'
    try:
        main()
    except Exception as e:
        if dev_mode:
            raise
        is_verbose = os.getenv("VERBOSE") == "1"
        if is_verbose:
            traceback.print_exc()
            sys.exit(1)
        echo(f'Error: {e}')
