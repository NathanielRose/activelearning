# Active Learning - Ensemble

## Quickstart

Ensure your paths `python` is >= `3.6.x`

### Install Dependencies

Install `virtualenv` and install project dependencies

```bash
pip install --upgrade pip virtualenv # upgrade/install pip and virtualenv
virtualenv .env # this will setup a local python installation in .env
source .env/bin/activate # shim the local python installation to your current session
pip install -r requirements.txt # pip now points to the pip locally installed in .env
```

### Run local development server

Create local sqlite database and run development server

```bash
./manage.py migrate # run any pending DB migrations or create the DB if not present
./manage.py runserver # run the local development server
```

### Optional: Install some test data

There are two ways to install some test data:

```bash
./manage.py loaddata fixtures.json # Fastest; loads a json file with some dummy data

# OR

./manage.py seeddata # More extensible; Custom command mapping to `ensemble/management/commands/seeddata.py`
```

## Access Admin Panel

Create a `superuser`

```bash
./manage.py createsuperuser # follow the prompts
```

Access admin panel at `localhost:8000/admin`

## IDE Configuration

### VSCode

Add the following to your workspace settings to configure `pylint` for a django project:

```json
"python.linting.pylintArgs": ["--load-plugins=pylint_django"]
```
