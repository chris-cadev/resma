from click import STRING, Context, argument, echo, group, option, pass_context
from click_aliases import ClickAliasedGroup

from resma.ingest.interfaces.factories.configuration_factory import make_ingest_configuration
from resma.ingest.interfaces.factories.ingest_controller_factory import make_ingest_reference_controller
from resma.shared.interfaces.factories.cache_path_factory import make_cache_path


@group(cls=ClickAliasedGroup)
@pass_context
def main(ctx):
    ctx.obj = {
        "env": make_ingest_configuration(),
        "cache_dir": make_cache_path(),
    }


@main.command(aliases=("ref", "r"))
@pass_context
@argument("url", type=STRING)
@option("--vault", "-v", type=STRING)
@option("--quiet", "-q", is_flag=True, default=False)
def reference_note(ctx: Context, url: str, vault: str, quiet: bool):
    env = ctx.obj['env']
    cache_dir = ctx.obj['cache_dir']
    vault = vault or env.default_vault
    try:
        ref_note = make_ingest_reference_controller(config=env, cache_dir=cache_dir).create_reference(
            url=url,
            vault=vault,
        )
        if not quiet:
            echo(ref_note.filepath)
    except SystemError as e:
        if not quiet:
            echo(e)


@main.command(aliases=("media", "m"))
@pass_context
@argument("url", type=STRING)
def media_file(ctx: Context, url: str):
    pass
