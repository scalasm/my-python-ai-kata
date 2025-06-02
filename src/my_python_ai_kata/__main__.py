"""Command-line interface."""

import click

@click.command()
@click.version_option()
def main() -> None:
    """My Python AI Sandbox."""
    print("My Python AI Sandbox is ready.")
                
if __name__ == "__main__":
    main(prog_name="my-python-ai-kata")  # pragma: no cover
