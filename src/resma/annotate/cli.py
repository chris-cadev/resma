from typing import Union
from click import Context, argument, option, group, STRING, pass_context
import click
from click_aliases import ClickAliasedGroup

from resma.annotate.interfaces.factories.note_controller_factory import make_create_note_controller, make_edit_note_controller
from resma.annotate.interfaces.factories.environment_factory import make_annotate_environment

env = make_annotate_environment()


@group(cls=ClickAliasedGroup, invoke_without_command=True)
@pass_context
@option('--name', '-n', type=STRING)
@option("--vault", "-v", type=STRING, default=env.default_vault)
def main(ctx: Context, name: Union[str, None] = None, vault: Union[str, None] = None):
    if not name:
        click.UsageError("Note name is required", ctx)
    if not ctx.invoked_subcommand:
        ctx.invoke(add_note, name=name, vault=vault, quiet=True)
        ctx.invoke(edit_note, name=name, vault=vault, quiet=False)


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
@option("--quiet", "-q", is_flag=True, default=False)
def add_note(ctx, name: str, vault: str, template: str = None, quiet: bool = False):
    controller = make_create_note_controller(ctx.obj.get('env'))
    note = controller.create_note(
        name=name,
        vault_name=vault,
        template=template,
    )
    if not quiet:
        click.echo(note.filepath)


@main.command(aliases=("edit", "en", "e"))
@pass_context
@argument("name", type=STRING, default=env.default_note_name)
@option(
    "--vault", "-v",
    default=env.default_vault,
    help="Vault name or directory path"
)
@option("--quiet", "-q", is_flag=True, default=False)
def edit_note(ctx, name: str, vault: str, quiet: bool = False):
    dto = make_edit_note_controller(
        ctx.obj.get('env')
    ).edit_note(
        name=name,
        vault=vault,
    )
    if not quiet:
        click.echo(dto.note.filepath)
