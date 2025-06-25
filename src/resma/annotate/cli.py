from click import argument, option, group, STRING, pass_context
import click
from click_aliases import ClickAliasedGroup

from resma.annotate.interfaces.factories.create_note_factory import make_create_note_controller
from resma.annotate.interfaces.factories.environment_factory import make_annotate_environment

env = make_annotate_environment()


@group(cls=ClickAliasedGroup)
@pass_context
def main(ctx):
    pass


@main.command(aliases=("nn", "n"))
@argument("name", type=STRING, default=env.default_note_name)
@option(
    "--vault", "-v",
    default=env.default_vault,
    help="Vault name or directory path"
)
@option(
    "--template",
    "-t",
    default=None,
    type=STRING,
    help="Template shortcut name",
)
@pass_context
def create_note(ctx, name: str, vault: str, template: str):
    controller = make_create_note_controller(ctx.obj.get('env'))
    note = controller.create_note(
        name=name,
        vault_name=vault,
        template=template
    )
    click.echo(note.filepath)
