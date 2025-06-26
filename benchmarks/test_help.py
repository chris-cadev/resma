from click.testing import CliRunner
from resma.cli import main


def test_resma_help(benchmark):
    runner = CliRunner()
    result = benchmark(lambda: runner.invoke(main, ("--help")))
    assert "Usage" in result.output


def test_resma_annotate_help(benchmark):
    runner = CliRunner()
    result = benchmark(lambda: runner.invoke(main, ("annotate", '--help')))
    assert "Usage" in result.output


def test_resma_annotate_add_help(benchmark):
    runner = CliRunner()
    result = benchmark(lambda: runner.invoke(
        main, ("annotate", "add", '--help')))
    assert "Usage" in result.output


def test_resma_annotate_edit_help(benchmark):
    runner = CliRunner()
    result = benchmark(lambda: runner.invoke(
        main, ("annotate", "edit", '--help')))
    assert "Usage" in result.output
