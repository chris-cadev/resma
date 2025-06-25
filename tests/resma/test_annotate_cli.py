from unittest.mock import patch
from click.testing import CliRunner
from resma.cli import main

def test_create_note_cli():
    mock_env = {
        "software": "path/to/software-vault"
    }

    with patch("resma.annotate.cli.ENV.VAULTS", mock_env):
        runner = CliRunner()
        result = runner.invoke(main, "annotate create-note example -v software")
        assert result.exit_code == 0
        assert "path/to/software-vault/example.md" in result.output
