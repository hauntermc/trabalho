from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from models import Base

# Carrega a configuração de logging do arquivo .ini
config = context.config
if config.config_file_name:
    fileConfig(config.config_file_name)

# Configura o target_metadata com os metadados da sua base
target_metadata = Base.metadata

# Configuração para execução de migrações offline
def run_migrations_offline():
    context.configure(
        url=config.get_main_option("sqlalchemy.url"),
        target_metadata=target_metadata,
        literal_binds=True
    )
    with context.begin_transaction():
        context.run_migrations()

# Configuração para execução de migrações online
def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )
        with context.begin_transaction():
            context.run_migrations()

# Verifica o modo de execução e decide qual método usar
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
