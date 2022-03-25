from contextlib import contextmanager
from os.path import dirname, abspath

from alembic.command import upgrade, downgrade
from alembic.config import Config


class Migration(object):
    def __init__(self):
        self.config = Config("alembic.ini")
        self.config.attributes['configure_logger'] = False
        self.config.set_main_option("script_location", "app/db/migrations")

    def upgrade(self, revision='head'):
        upgrade(self.config, revision)

    def downgrade(self, revision='base'):
        downgrade(self.config, revision)

    def alembic_file_path(self, alembic):
        d = dirname(dirname(abspath(__file__)))
        return "{}/{}".format(d, alembic)


@contextmanager
def reset_db():  # pragma: no cover
    m = Migration()
    m.upgrade()
    yield
    m.downgrade()
