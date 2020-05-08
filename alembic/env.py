import sys
from logging.config import fileConfig

from alembic import context
from plumbum import local
from sqlalchemy import engine_from_config, pool, create_engine

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add repo root to path to ensure our project files are imported correctly
parent_dir = local.path(__file__).dirname.up()
sys.path.append(parent_dir)

# this will overwrite the ini-file sqlalchemy.url path
# with the path given in the config of the main code
from nexml_nyiso.utility import get_url

config.set_main_option('sqlalchemy.url', get_url())

# add your model's MetaData object here
# for 'autogenerate' support
from nexml_nyiso import model
target_metadata = model.Base.metadata


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = create_engine(get_url())

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
