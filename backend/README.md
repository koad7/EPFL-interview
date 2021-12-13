# resslab_tools

## Database Migration

```bash
# Generate new revision
poetry run dotenv -f ../secrets/.env run alembic revision --autogenerate -m "kodjo_change"

# Manually upgrade database (automatically run at startup)
poetry run dotenv -f ../secrets/.env run alembic upgrade head

# Downgrade https://alembic.sqlalchemy.org/en/latest/tutorial.html#downgrading
poetry run dotenv -f ../secrets/.env run alembic downgrade
```

## Upload data

```bash
poetry run dotenv -f ../secrets/.env run python data.py connection ../data/connections_located.csv
poetry run dotenv -f ../secrets/.env run python data.py connection-global ../data/Global/*.csv
poetry run dotenv -f ../secrets/.env run python data.py connection-panel-zone ../data/Panel_zone/*.csv
```
