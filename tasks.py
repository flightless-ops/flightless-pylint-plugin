from invoke.tasks import task
from invoke.context import Context


@task
def flake8(context: Context) -> None:
    context.run("poetry run flake8 .")


@task
def pylint(context: Context) -> None:
    context.run("poetry run pylint .")


@task
def mypy(context: Context) -> None:
    context.run("poetry run mypy .")


@task(
    flake8,
    pylint,
    mypy,
)
def lint(_context: Context) -> None: ...


@task
def test(context: Context) -> None:
    context.run("poetry run pytest")


@task
def coverage(context: Context) -> None:
    context.run(
        "poetry run pytest --cov=flightless_pylint_plugin --cov-report=html --cov-report=term-missing"
    )


@task
def build(context: Context) -> None:
    context.run("poetry build")


@task
def publish(context: Context) -> None:
    context.run("poetry publish")
