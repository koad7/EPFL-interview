"""
Dynaconf Settings
"""
from dynaconf import Dynaconf, Validator

settings = Dynaconf(
    envvar_prefix=False,
    settings_files=['resslab_tools/settings.toml'],
    validators=[
        Validator('cors_enabled', default=False),
        Validator('root_path', default=''),
        Validator('database_host', default='localhost'),
        Validator('database_port', default=5432),
        Validator('postgres_user', default='postgres'),
        Validator('postgres_password', must_exist=True),
        Validator('postgres_db', default='postgres'),
    ],
)

# `envvar_prefix` = export envvars with `export DYNACONF_FOO=bar`.
# `settings_files` = Load these files in the order.
