install:
	poetry install

run:
	poetry run dotenv -f ../secrets/.env run uvicorn resslab_tools.main:app --reload

test:
	poetry run pytest

upload-data:
	poetry run dotenv -f ../secrets/.env run python data.py connection ../data/connections_located.csv
	poetry run dotenv -f ../secrets/.env run python data.py connection ../data/connections_located.csv
	poetry run dotenv -f ../secrets/.env run python data.py connection-global ../data/Global/*.csv
	poetry run dotenv -f ../secrets/.env run python data.py connection-panel-zone ../data/Panel_zone/*.csv
