from click.testing import CliRunner
from resma.cli import main


def test_main_version():
    runner = CliRunner()
    result = runner.invoke(main, "--version")
    assert result.exit_code == 0
    assert "resma: Range Signal Meta Amplifier, version 0.0.0" in result.output


def test_subcommands_showing():
    runner = CliRunner()
    result = runner.invoke(main, ['--help'])
    assert result.exit_code == 0
    assert "annotate" in result.output
    assert "ingest" in result.output
    assert "publish" in result.output
