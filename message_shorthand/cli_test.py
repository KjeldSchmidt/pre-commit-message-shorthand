"""
Tests for the message shorthand argument parsing functionality.

This represents the most immediate public interface of the application.
"""

from __future__ import annotations

import json
import secrets
import string
from pathlib import Path
from typing import TYPE_CHECKING
from unittest.mock import call

from click.testing import CliRunner

if TYPE_CHECKING:
    from pytest_mock import MockerFixture

from message_shorthand import main

CLICK_FAILURE_CODE = 2
COMMIT_MSG_FILE_NAME = "commit-msg"
COMMIT_MSG_FILE_PATH = Path(COMMIT_MSG_FILE_NAME)


def test_fails_on_no_input() -> None:
    runner = CliRunner()
    result = runner.invoke(main, [])
    assert "Missing argument 'SUBSTITUTIONS'" in result.output
    assert result.exit_code == CLICK_FAILURE_CODE


def test_fails_on_no_input_file() -> None:
    runner = CliRunner()
    result = runner.invoke(main, ["{}"])
    assert "Missing argument 'COMMIT_MSG_FILE'" in result.output
    assert result.exit_code == CLICK_FAILURE_CODE


def test_fails_on_no_nonexistent_file() -> None:
    runner = CliRunner()
    result = runner.invoke(main, ["{}", ""])
    assert "File '' does not exist." in result.output
    assert result.exit_code == CLICK_FAILURE_CODE


def test_fails_on_missing_file() -> None:
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(main, ["{}", COMMIT_MSG_FILE_NAME])
        assert f"File '{COMMIT_MSG_FILE_NAME}' does not exist." in result.output
        assert result.exit_code == CLICK_FAILURE_CODE


def test_accepts_empty_substitutions() -> None:
    runner = CliRunner()
    original_file_content = "Original Content"
    with runner.isolated_filesystem():
        write_input_file(original_file_content)

        result = runner.invoke(main, ["{}", COMMIT_MSG_FILE_NAME])

        assert result.exit_code == 0
        assert read_input_file() == original_file_content


def test_rewrites_input_file() -> None:
    runner = CliRunner()
    original_file_content = "Original Content"
    with runner.isolated_filesystem():
        write_input_file(original_file_content)

        result = runner.invoke(main, ['{"Original": "Modified"}', COMMIT_MSG_FILE_NAME])

        assert result.exit_code == 0
        assert read_input_file() == "Modified Content"


def test_raises_error_for_invalid_substitutions() -> None:
    runner = CliRunner()
    original_file_content = "Original Content"
    substitutions_input = '{"key": "value", "obj_key": {}}'
    with runner.isolated_filesystem():
        write_input_file(original_file_content)

        result = runner.invoke(main, [substitutions_input, COMMIT_MSG_FILE_NAME])

        assert "Substitutions do not map from string to string" in str(result.exception)
        assert result.exit_code == 1
        assert read_input_file() == original_file_content


def test_raises_error_for_malformed_substitutions() -> None:
    runner = CliRunner()
    original_file_content = "Original Content"
    substitutions_input = '{"key":}'
    with runner.isolated_filesystem():
        write_input_file(original_file_content)

        result = runner.invoke(main, [substitutions_input, COMMIT_MSG_FILE_NAME])

        assert "The provided substitution map is not valid JSON" in str(
            result.exception
        )
        assert result.exit_code == 1
        assert read_input_file() == original_file_content


def test_delegates_substitution_appropriately(mocker: MockerFixture) -> None:
    runner = CliRunner()
    original_file_content = "Original Content"
    substitute_mock = mocker.Mock()
    mocker.patch("message_shorthand.substitute_commit_msg", substitute_mock)
    random_substitution_map = generate_random_substitution_map()
    with runner.isolated_filesystem():
        write_input_file(original_file_content)

        runner.invoke(main, [json.dumps(random_substitution_map), COMMIT_MSG_FILE_NAME])

        assert substitute_mock.call_args_list == [
            call(original_file_content, random_substitution_map)
        ]


def write_input_file(content: str) -> None:
    with Path.open(COMMIT_MSG_FILE_PATH, "w") as file:
        file.write(content)


def read_input_file() -> str:
    with Path.open(COMMIT_MSG_FILE_PATH) as file:
        return file.read()


def generate_random_substitution_map() -> dict[str, str]:
    random_substitutions = {}
    substitution_count = secrets.randbelow(100)
    for _ in range(substitution_count):
        key_length = secrets.randbelow(20)
        value_length = secrets.randbelow(20)
        key = random_word(key_length)
        value = random_word(value_length)
        random_substitutions[key] = value
    return random_substitutions


def random_word(length: int) -> str:
    letters = string.ascii_letters + string.digits
    return "".join(secrets.choice(letters) for _ in range(length))
