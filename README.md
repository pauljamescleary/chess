# Backend

## Getting started

1. Python 3.9 installed.  Later versions of python may have issues.  Run `python3 --version`
2. Install [Poetry](https://python-poetry.org/) - this is used for package management, no more messing with virtualenvs!
3. If using zsh, may need to `export SHELL=/bin/zsh`
4. Run `poetry install` - this will create a virtualenv and download all the dependenies
5. Run `poetry shell` to enter into the virtualenv.  **important**

## Running the tests

The tests are built using [pytest](https://docs.pytest.org/en/7.2.x/).  The tests uses sqllite running in memory, 
as such you do not need to spin up a database.

To execute tests, simply run `pytest`

## Running the app

You can run the app via flask, hitting a "real" postgres database

1. Run `docker-compose up -d db` to start up the postgres database
2. Run `flask db migrate` to run migrations and get the database ready
3. Use `example.http` to run commands to test the API
4. 