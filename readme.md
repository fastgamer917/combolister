## Installation

1. install poetry first `pip install poetry`
   2. If you get error unable to install system-wide packages, then do this: `sudo apt install python3-poetry`. Then good to go.
2. install dependencies and venv with poetry: `poetry install`
3. create a folder called `toupload` inside parent directory. i.e main combolister dir.
4. places all files to upload in this 3.

## Poetry Settings
1. `poetry config virtualenvs.in-project true` 
2. `poetry run python manage.py runserver`

## Run Migrations
1. now since all setup, run migrations.