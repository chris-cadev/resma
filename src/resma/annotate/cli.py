from click import argument, option, group, STRING
from click_aliases import ClickAliasedGroup

from resma.annotate.environment import AnnotateEnvironment

ENV = AnnotateEnvironment()


@group(cls=ClickAliasedGroup)
def main():
    pass


@main.command(aliases=("nn", "n"))
@argument("name", type=STRING, default=ENV.ANNOTATE_UNTITLED_NAME)
@option(
    "--vault", "-v",
    default=ENV.ANNOTATE_DEFAULT_VAULT,
    help="Vault name or directory path"
)
@option(
    "--template",
    "-t",
    default=None,
    type=STRING,
    help="Template shortcut name",
)
def create_note(name: str, vault: str, template: str):
    print(f"{ENV.VAULTS[vault]}/{name}.md")
