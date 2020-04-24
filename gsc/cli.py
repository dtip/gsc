import typer
import gsc
from gsc import auth, client, verifier

app = typer.Typer()


def success(msg: str):
    typer.secho(msg, fg=typer.colors.GREEN, bold=True)


def info(msg: str):
    typer.echo(msg)


def title(msg: str):
    typer.secho(msg + "\n", fg=typer.colors.GREEN, bold=True)


def warn(msg: str):
    typer.secho(msg + "\n", fg=typer.colors.YELLOW, bold=False)


def error(msg: str):
    typer.secho(msg, fg=typer.colors.RED, bold=True)
    raise typer.Exit(1)


@app.command()
def login(email: str = typer.Option(..., prompt=True)):
    try:
        auth.login(email)
        success("🎉 Login Success.")
    except auth.AuthenticationError as e:
        error(str(e))


@app.command()
def ping():
    try:
        client.ping()
        success("Pong.")
    except auth.AuthenticationError as e:
        error(str(e))
    except client.APIError as e:
        error(str(e))


@app.command()
def verify():
    try:
        client.ping()
        verifier.verify()
        success("✔️  Exercise complete!")
    except verifier.VerifyError as e:
        error(str(e))
    except auth.AuthenticationError as e:
        error(str(e))
    except client.APIError as e:
        error(str(e))


@app.callback()
def version_callback(value: bool):
    if value:
        version()


@app.command(hidden=True)
def version():
    typer.echo(f"gsc version: {gsc.__version__}")
    raise typer.Exit()


@app.callback()
def options(version: bool = typer.Option(None, "--version", callback=version_callback)):
    """
    gsc is the Git for Scientists practical exercise helper.

    See https://www.gitscientist.com for more.
    """


def main():
    app()
