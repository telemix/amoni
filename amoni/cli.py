# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Amoni project team members listed at
# https://github.com/anvilistas/amoni/graphs/contributors
#
# This software is published at https://github.com/anvilistas/amoni
from pathlib import Path

import typer
from cookiecutter.exceptions import OutputDirExistsException

from . import api
from .stubs import generate_tables

__version__ = "0.0.4"

amoni = typer.Typer()


@amoni.callback()
def main():
    pass


@amoni.command()
def init(
    directory: Path = typer.Argument(
        ..., file_okay=False, resolve_path=True, help="Directory to initialiase"
    ),
    app: str = typer.Argument("hello_world", help="App Folder Name"),
):
    try:
        api.init(directory, app)
        typer.echo(f"Amoni project created in {directory}\nDone! ✨")
    except OutputDirExistsException:
        msg = f"Error creating project:\n{directory} already exists"
        typer.secho(msg, fg=typer.colors.RED)


@amoni.command()
def start():
    """Start the anvil app and db servers"""
    typer.echo("Rebuilding server images")
    api.build_image("app")
    api.pull_image("db")
    typer.echo("Starting anvil app and database servers")
    api.start_service("app", detach=True)
    typer.echo("Your app is available at http://localhost:3030")


@amoni.command()
def stop():
    """Stop the anvil app and db servers"""
    typer.echo("Stopping the anvil app and database servers")
    api.stop_services()


@amoni.command()
def test():
    """Run the test suite"""
    typer.echo("Checking for newer images")
    service = "test_runner"
    api.build_image(service)
    api.run_service(service)


@amoni.command()
def generate():
    """Generate stubs for the database"""
    msg = generate_tables()
    typer.echo(msg)
