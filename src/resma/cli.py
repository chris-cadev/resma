import importlib

from click import group, pass_context, version_option
from click_aliases import ClickAliasedGroup

from resma.annotate.interfaces.factories.environment_factory import make_annotate_environment
from resma.ingest.cli import main as main_ingest
from resma.annotate.cli import main as main_annotate
from resma.publish.cli import main as main_publish


@group(cls=ClickAliasedGroup)
@version_option(version=importlib.metadata.version('resma'), prog_name='resma: Range Signal Meta Amplifier')
@pass_context
def main(ctx):
    ctx.obj = {
        "env": make_annotate_environment()
    }



commands = {
    'ingest': main_ingest,  # bibliography
    'annotate': main_annotate,  # notes new
    'publish': main_publish,  # gather scatter
}


for name in commands.keys():
    main.add_command(commands.get(name), name)
if __name__ == '__main__':
    main()
