from typing import Union
from click import Context, argument, option, group, STRING, pass_context
import click
from click_aliases import ClickAliasedGroup

from resma.annotate.interfaces.factories.note_controller_factory import make_create_note_controller, make_edit_note_controller
from resma.annotate.interfaces.factories.configuration_factory import make_annotate_configuration

env = make_annotate_configuration()


@group(cls=ClickAliasedGroup)
@pass_context
def main(ctx):
    pass


@main.command(aliases=("open", "o"))
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
def open_note(ctx: Context, name: str, vault: str, template: str = None, quiet: bool = False):
    ctx.invoke(
        add_note,
        name=name, vault=vault,
        template=template, quiet=True,
    )
    ctx.invoke(
        edit_note,
        name=name, vault=vault,
        quiet=quiet,
    )



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
