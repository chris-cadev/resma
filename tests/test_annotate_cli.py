import os
from unittest.mock import patch, MagicMock
from click.testing import CliRunner
from resma.cli import main


def test_create_note_cli():
    test_vault_directory = f"{os.path.dirname(__file__)}/.test-data/software-vault"
    mock_env = MagicMock()
    mock_env.default_note_name = "example"
    mock_env.default_vault = "software"
    mock_env.vaults = {
        "software": test_vault_directory
    }

    with patch("resma.cli.make_annotate_environment", return_value=mock_env):
        runner = CliRunner()
        result = runner.invoke(
            main, ["annotate", "create-note", "example", "-v", "software"], obj={"env": mock_env})
        assert result.exit_code == 0
        assert f"{test_vault_directory}/example.md" in result.output
