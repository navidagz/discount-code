from alembic import command
from alembic.config import Config


ALEMBIC_INI_PATH = 'alembic.ini'


def run_db_migrations():  # pragma: no cover
    alembic_cfg = Config(ALEMBIC_INI_PATH)
    command.upgrade(alembic_cfg, 'head')


def startup():
    run_db_migrations()
