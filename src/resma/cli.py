import click
import importlib

from click_aliases import ClickAliasedGroup


@click.group(cls=ClickAliasedGroup)
@click.version_option(version=importlib.metadata.version('resma'), prog_name='resma: Range Signal Meta Amplifier')
def main():
    print('hello world')


if __name__ == '__main__':
    main()
