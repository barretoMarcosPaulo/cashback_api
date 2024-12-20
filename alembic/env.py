from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
from app.infrastructure.database import Base
from app.models.user import UserSellerModel
from app.models.order import OrdersModel

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


target_metadata = Base.metadata

def run_migrations_offline() -> None:
    url = DATABASE_URL 
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    connectable = create_async_engine(DATABASE_URL)

    async with connectable.connect() as connection:
        await connection.run_sync(
            lambda conn: context.configure(
                connection=conn,
                target_metadata=target_metadata
            )
        )
        async with connection.begin():
            await connection.run_sync(context.run_migrations)

def run_migrations_online() -> None:
    sync_database_url = DATABASE_URL.replace("asyncpg", "psycopg2")

    connectable = create_engine(sync_database_url)

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
