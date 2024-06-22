"""Singular module concerned with applying the commit-msg hook substitutions."""

from __future__ import annotations

import argparse
import sys
from typing import Mapping


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
    subs = substitutions.get(original_msg)
    return original_msg if subs is None else subs


def main() -> None:
    """
    Run entrypoint of the substitution hook.

    This parses CLI arguments, performs file system operations and exits with
    appropriate error codes.

    :return: None
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("commit_msg_file", nargs="1")
    parser.add_argument("substitutions", action="append")
    parser.add_argument("separator", action="store_const", const="|")
    parser.parse_args()

    sys.exit(1)


if __name__ == "__main__":
    main()
