"""
Tests for the message shorthand substitution functionality.

These are focused on the substitution of the string and ignore the
file system interaction.
"""

from message_shorthand import substitute_commit_msg


def test_returns_empty_string_for_empty_input() -> None:
    original_msg = ""
    substitutions: dict[str, str] = {}

    result = substitute_commit_msg(original_msg, substitutions)
    assert result == ""


def test_returns_original_msg_for_empty_substitutions() -> None:
    original_msg = "original_msg"
    substitutions: dict[str, str] = {}

    result = substitute_commit_msg(original_msg, substitutions)
    assert result == original_msg


def test_returns_original_msg_for_non_matching_substitutions() -> None:
    original_msg = "ABCD"
    substitutions = {"E": "F"}

    result = substitute_commit_msg(original_msg, substitutions)
    assert result == original_msg


def test_returns_modified_msg_for_one_matching_substitution() -> None:
    original_msg = "ABCD"
    substitutions = {"A": "B"}

    result = substitute_commit_msg(original_msg, substitutions)
    assert result == "BBCD"


def test_applies_substitution_multiple_times() -> None:
    original_msg = "ABCDA"
    substitutions = {"A": "B"}

    result = substitute_commit_msg(original_msg, substitutions)
    assert result == "BBCDB"


def test_applies_multiple_substitutions() -> None:
    original_msg = "ABCD"
    substitutions = {"A": "B", "C": "D"}

    result = substitute_commit_msg(original_msg, substitutions)
    assert result == "BBDD"


def test_applies_multiple_substitutions_multiple_times() -> None:
    original_msg = "ABCDABCD"
    substitutions = {"A": "B", "C": "D"}

    result = substitute_commit_msg(original_msg, substitutions)
    assert result == "BBDDBBDD"
