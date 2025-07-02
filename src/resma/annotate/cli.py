from click import Context, argument, option, group, STRING, pass_context
import click
from click_aliases import ClickAliasedGroup

from resma.annotate.interfaces.factories.configuration_factory import make_annotate_configuration
from resma.annotate.interfaces.factories.note_controller_factory import (
    make_create_note_controller as create_note_ctl,
    make_create_template_note_controller as create_template_note_ctl,
    make_edit_note_controller as edit_note_ctl,
)


@group(cls=ClickAliasedGroup)
@pass_context
def main(ctx: Context):
    ctx.obj = {
        "env": make_annotate_configuration()
    }

@main.command(aliases=("open", "o"))
@pass_context
@argument("name", type=STRING, required=False)
@option("--vault", "-v", required=False, help="Vault name or directory path")
@option("--template", "-t", type=STRING, required=False, help="Template shortcut name")
@option("--quiet", "-q", is_flag=True, default=False)
def open_note(ctx: Context, name: str, vault: str, template: str = None, quiet: bool = False):
    env = ctx.obj["env"]
    name = name or env.default_note_name
    vault = vault or env.default_vault
    try:
        ctx.invoke(add_note, name=name, vault=vault,
                   template=template, quiet=True)
    finally:
        ctx.invoke(edit_note, name=name, vault=vault, quiet=quiet)


@main.command(aliases=("add", "an", "a"))
@pass_context
@argument("name", type=STRING, required=False)
@option("--vault", "-v", required=False, help="Vault name or directory path")
@option("--template", "-t", type=STRING, required=False, help="Template shortcut name")
@option("--extra", "-e", type=(str, str), multiple=True)
@option("--quiet", "-q", is_flag=True, default=False)
def add_note(ctx: Context, name: str, vault: str, template: str = None, extra: tuple[str] = (), quiet: bool = False):
    env = ctx.obj["env"]
    name = name or env.default_note_name
    vault = vault or env.default_vault

    if not template:
        note = create_note_ctl(env).create_note(
            name=name, vault=vault
        )
    else:
        meta = dict(extra)
        note = create_template_note_ctl(env).create_note(
            name=name, vault=vault, template=template, meta=meta)
    if not quiet and note:
        click.echo(note.filepath)


@main.command(aliases=("edit", "en", "e"))
@pass_context
@argument("name", type=STRING, required=True)
@option("--vault", "-v", required=False, help="Vault name or directory path")
@option("--quiet", "-q", is_flag=True, default=False)
def edit_note(ctx: Context, name: str, vault: str, quiet: bool = False):
    env = ctx.obj["env"]
    vault = vault or env.default_vault

    dto = edit_note_ctl(env).edit_note(name=name, vault=vault)

    if not quiet:
        click.echo(dto.filepath)
