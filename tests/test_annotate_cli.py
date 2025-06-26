import os
from unittest.mock import patch, MagicMock
from click.testing import CliRunner
from resma.cli import main

testing_vault_name = 'RAKMA'
test_workspace = f"{os.path.dirname(__file__)}/.test-data"
test_vault_path = testing_vault_name.lower()


def clean_filepath(filepath: str):
    if os.path.exists(filepath):
        os.remove(filepath)
    if os.path.exists(filepath):
        os.removedirs(os.path.dirname(filepath))


def test_add_note_cli():
    mock_env = MagicMock()
    mock_env.vaults = {
        f'{testing_vault_name}': test_vault_path
    }
    mock_env.workspace = test_workspace
    expected_filepath = os.path.join(
        test_workspace, test_vault_path, "add-example.md"
    )

    try:
        with patch("resma.cli.make_annotate_configuration", return_value=mock_env):
            runner = CliRunner()
            result = runner.invoke(
                main, (
                    "annotate", "add-note", "add-example",
                    "-v", testing_vault_name
                ), obj={"env": mock_env})
            assert result.exit_code == 0
            assert expected_filepath in result.output
    finally:
        clean_filepath(expected_filepath)


def test_edit_note_cli():
    mock_env = MagicMock()
    mock_env.vaults = {
        f'{testing_vault_name}': test_vault_path
    }
    mock_env.workspace = test_workspace
    mock_env.editor_cmd = "nvim"
    expected_filepath = os.path.join(
        test_workspace, test_vault_path, "edit-example.md"
    )

    try:
        with patch("resma.cli.make_annotate_configuration", return_value=mock_env):
            with patch("os.system") as mock_system:
                runner = CliRunner()
                runner.invoke(
                    main,
                    (
                        "annotate", "add-note", "edit-example",
                        "-v", testing_vault_name,
                    ),
                    obj={"env": mock_env},
                )
                result = runner.invoke(
                    main,
                    (
                        "annotate", "edit-note", "edit-example",
                        "-v", testing_vault_name,
                    ),
                    obj={"env": mock_env},
                )

                assert result.exit_code == 0
                assert expected_filepath in result.output

                expected_cmd = f'{mock_env.editor_cmd} "{expected_filepath}"'
                mock_system.assert_called_with(expected_cmd)
    finally:
        clean_filepath(expected_filepath)


def test_open_note_cli():
    mock_env = MagicMock()
    mock_env.vaults = {
        f'{testing_vault_name}': test_vault_path
    }
    mock_env.workspace = test_workspace
    mock_env.editor_cmd = "nvim"
    expected_filepath = os.path.join(
        test_workspace, test_vault_path, "open-example.md"
    )

    try:
        with patch("resma.cli.make_annotate_configuration", return_value=mock_env):
            with patch("os.system") as mock_system:
                runner = CliRunner()
                result = runner.invoke(
                    main,
                    (
                        "annotate", "open-note", "open-example",
                        "-v", testing_vault_name
                    ),
                    obj={"env": mock_env},
                )

                assert result.exit_code == 0
                assert expected_filepath in result.output

                expected_cmd = f'{mock_env.editor_cmd} "{expected_filepath}"'
                mock_system.assert_called_with(expected_cmd)
    finally:
        clean_filepath(expected_filepath)
