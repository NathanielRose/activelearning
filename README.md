# Active Learning - Ensemble

## Quickstart

### System Requirements

| Requirement | Version    | Misc                                           |
| ----------- | ---------- | ---------------------------------------------- |
| Python      | >= `3.6.0` |                                                |
| Node        | `LTS`      | Used for building the front-end visualizations |

### Install Dependencies

Install `virtualenv` and install project dependencies

```bash
pip install --upgrade pip virtualenv # upgrade/install pip and virtualenv
virtualenv .env # this will setup a local python installation in .env
source .env/bin/activate # shim the local python installation to your current session
pip install -r requirements.txt # pip now points to the pip locally installed in .env
```

### Build the Front-End Visualization

The front end visualization is a react application built using [create-react-app](https://github.com/facebook/create-react-app)

```bash
./manage.py buildfrontend # runs the build script found in `ensemble/management/commands/buildfrontend.py`
```

### Run local development server

Create local sqlite database and run development server

```bash
./manage.py migrate # run any pending DB migrations or create the DB if not present
./manage.py runserver # At this point, you have everything you'll need to run the local development server
```

## Parsing Ensemble JSON files & Creating some test data

There is currently a script/command to import/parse ensemble JSON files located at `ensemble/management/commands/parseensemblejson.py`

There are some ensemble json files for Deadpool2 and Predator located in `ensemble/static/ensemble`

```bash
./manage.py parseensemblejson \
  ensemble/static/ensemble/ensemble_inference.json \
  ensemble/static/ensemble/ensemble_ground_truth.json \
  ensemble/static/ensemble/ensemble_custom_model.json \
  ensemble/static/ensemble/ensemble_custom_vision.json \
  ensemble/static/ensemble/ensemble_keras2s_13a_deadpool2.json \
  ensemble/static/ensemble/ensemble_keras2d_13a_predator.json
```

## Access Admin Panel

Create a `superuser`

```bash
./manage.py createsuperuser # follow the prompts
```

Access admin panel at `localhost:8000/admin`

## Project Layout

| Directory                                 | Purpose                                                                                                                                           | Notes |
| ----------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- | ----- |
| activelearning                            | The main Django Project; binds together smaller applications                                                                                      |
| ensemble                                  | The application holding the visualization and model code for the ensemble                                                                         |
| ensemble/static/ensemble/foxmovieensemble | The front end project containing the React application used for visualizations. The ensemble application serves the build files from this project |

## IDE Configuration

### VSCode

Add the following to your workspace settings to configure `pylint` for a django project:

```json
"python.linting.pylintArgs": ["--load-plugins=pylint_django"]
```
