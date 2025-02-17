# alembic/env.py

from app.core.database import Base
from app.core.config import settings
from alembic import context
from app.models.user import User
from app.models.referral import Referral
from app.models.referral_code import ReferralCode
from sqlalchemy import engine_from_config, pool
from logging.config import fileConfig


config = context.config
fileConfig(config.config_file_name)

target_metadata = Base.metadata


def get_url():
    return settings.SYNC_DATABASE_URL


def run_migrations_offline():
    url = get_url()
    context.configure(url=url, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    config.set_main_option('sqlalchemy.url', get_url())
    engine = engine_from_config(config.get_section(
        config.config_ini_section), prefix='sqlalchemy.', poolclass=pool.NullPool)
    with engine.connect() as connection:
        context.configure(connection=connection,
                          target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
