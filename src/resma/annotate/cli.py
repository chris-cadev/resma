from click import argument, option, group, STRING, pass_context
import click
from click_aliases import ClickAliasedGroup

from resma.annotate.interfaces.factories.note_controller_factory import make_create_note_controller, make_edit_note_controller
from resma.annotate.interfaces.factories.environment_factory import make_annotate_environment

env = make_annotate_environment()


@group(cls=ClickAliasedGroup)
@pass_context
def main(ctx):
    pass


@main.command(aliases=("add", "an", "a"))
@pass_context
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
def add_note(ctx, name: str, vault: str, template: str):
    controller = make_create_note_controller(ctx.obj.get('env'))
    note = controller.create_note(
        name=name,
        vault_name=vault,
        template=template,
    )
    click.echo(note.filepath)


@main.command(aliases=("edit", "en", "e"))
@pass_context
@argument("name", type=STRING, default=env.default_note_name)
@option(
    "--vault", "-v",
    default=env.default_vault,
    help="Vault name or directory path"
)
def edit_note(ctx, name: str, vault: str):
    dto = make_edit_note_controller(
        ctx.obj.get('env')
    ).edit_note(
        name=name,
        vault=vault,
    )
    click.echo(dto.note.filepath)
