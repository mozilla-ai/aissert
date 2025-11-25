"""Main CLI entry point for example package."""

from example_pkg.generators import gen_use_local_llamafile


def main_cli() -> None:
    """CLI main function."""
    # TODO start llamafile and wait for it to become available
    print(gen_use_local_llamafile()())
