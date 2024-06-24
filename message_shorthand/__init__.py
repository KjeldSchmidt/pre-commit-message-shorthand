"""Singular module concerned with applying the commit-msg hook substitutions."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Mapping

import click

from message_shorthand.errors import (
    SubstitutionMapInvalidError,
    SubstitutionMapJsonError,
)


def substitute_commit_msg(
    original_msg: str,
    substitutions: Mapping[str, str],
) -> str:
    """
    Apply string-level substitution based on a dictionary.

    Occurrences of the keys of the substitution mapping in the original_msg will
    be replaced in the result string.

    Substitutions are applied in order of iteration for the mapping.
    If earlier substitutions introduce new text that matches the key of a
    later substitution, this will be substituted in the final string.
    If the order is reversed, this does not happen.

    Args:
        original_msg: The original string in which substitutions will be applied
        substitutions: A mapping of substitution pairs.

    Returns:
        The input string after all substitution have been applied.
    """
    modified_message = original_msg
    for string_to_replace, replacement in substitutions.items():
        modified_message = modified_message.replace(string_to_replace, replacement)
    return modified_message


@click.command()
@click.argument(
    "commit_msg_file",
    type=click.Path(
        exists=True,
        writable=True,
        readable=True,
        dir_okay=False,
        path_type=Path,
    ),
)
@click.argument("substitutions")
def main(commit_msg_file: Path, substitutions: str) -> None:
    """
    Substitute strings in COMMIT_MESSAGE_FILE according to SUBSTITUTIONS.

    COMMIT_MESSAGE_FILE is a path to the commit message that is to be rewritten.
    It should be the same value that is originally passed to the commit-msg hook
    by git.

    SUBSTITUTIONS is a JSON-encoded dictionary of strings. Occurrences of keys
    from this dictionary in the content of COMMIT_MESSAGE_FILE will be replaced
    by their corresponding values.
    """
    with Path.open(commit_msg_file, "r") as file:
        commit_msg = file.read()
    substitutions_dict = parse_and_validate_substitutions(substitutions)

    new_message = substitute_commit_msg(commit_msg, substitutions_dict)
    with Path.open(commit_msg_file, "w") as file:
        file.write(new_message)


def parse_and_validate_substitutions(substitutions_string: str) -> dict[str, str]:
    """
    Parse the substitutions JSON input.

    Additionally, raise an error if not all keys and values are strings.

    Args:
        substitutions_string: A JSON-encoded representation of the substitutions
            dictionary.

    Returns:
        A dict[str, str] representation of the input

    Raises:
        ValueError if any of the keys/values of the input are not strings
        json.JSONDecodeError if the input is not well-formed JSON

    """
    try:
        parsed_dict: dict[str, str] = json.loads(substitutions_string)
    except json.JSONDecodeError as exception:
        raise SubstitutionMapJsonError from exception

    for key, value in parsed_dict.items():
        if not isinstance(key, str) or not isinstance(value, str):
            raise SubstitutionMapInvalidError
    return parsed_dict


if __name__ == "__main__":
    main()
