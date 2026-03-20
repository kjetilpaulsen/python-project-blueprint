# python-project-blueprint

This repo was originally intended to be kept privat, so I am in the process of rewriting this README.md. The README.md should be updated by March 23, 2026.

A blueprint for creating python projects. Copy the contents of this repo into a new python project, and use this as a starting point for your project. Remember to search and replace through the files for ```python-project-blueprint``` for app name, and ```python_project_blueprint``` for package name.

## Features
- Two Entrypoints, CLI & FastAPI
- XDG folder structure for logs, config, data, cache/tmp
- Different logging-setups can be specified(file, console, stderr)
- Command/Event architecture to handle instructions and results
- Includes testing for the initial blueprints
- Includes dockerfile and docker-compose
- Includes a workflow that run tests, build docker image and publishes to dockerhub if pushed to a release-branch

## Installation

### Requirements
- **Python** ≥ 3.11 (recommended: 3.12–3.14)
- **uv** (for dependency and environment management)

### Setup
```bash
git clone https://github.com/kjetilpaulsen/python-project-blueprint.git
cd python-project-blueprint
uv sync
```
*Optionally you can activate the virtual environment:*
```
source .venv/bin/activate
```
To see the list of available commands:

```
uv run python -m python_project_blueprint cli -h
```
You now have a couple of options for how to run the app. Since this is a foundation for other projects, it only has one command, ```version```, with one optional command ```--uppercase```. It will return an event that contains the version of the app and the "v" infront of the version is either uppercase or lowercase.

To test in CLI mode:
```
uv run python -m python_project_blueprint cli version
```

To test in API mode:
```
uv run python -m python_project_blueprint api
```
Or with spesific host, port and reload:
```
uv run python -m python_project_blueprint api \
  --host 127.0.0.1 \
  --port 8001 \
  --reload
```
This can then be tested with curl like so:
```
curl http://127.0.0.1:8001/health
```
And the ```version``` can be tested by running the command:
```
curl -X POST http://127.0.0.1:8001/run \
  -H "Content-Type: application/json" \
  -d '{
    "commands": [
      { "name": "version", "options": {} }
    ]
  }'
```
If you want the app to build a config file in ```~/.config/python-project-blueprint/python_project_blueprint.conf```:
```
uv run python -m python_project_blueprint cli --build-config
```
The app also supports testing with pytest:
```
uv run pytest
```
or with coverage:
```
uv run pytest -V --cov=python_project_blueprint --cov-report=term-missing
```

## Docker & GitHub Actions Setup

### Overview

- **Docker**: Used to build and run the API locally
- **Docker Compose**: Runs the API container (no database required)
- **GitHub Actions**: Runs tests and builds/pushes Docker images on `release` branch

---

## Local Docker Usage

### 1. Create `.env`

```env
IMAGE_NAME=<your-dockerhub-username>/<your-image-name>
IMAGE_TAG=latest

# App settings (optional)
LOG_LEVEL=DEBUG
CONSOLE_LOG=true
STDERR_LOG=true
```
### 2. Build, run and test the image and container
Build the image and run the container:
```
docker compose up --build
```
And stop it like so:
```
docker compose down
```
Test the API entrypoint while running the container like so:
```
curl http://127.0.0.1:8010/health
```

## Github Actions usage

### 1. Setup secrets in your repo
Navigate to secrets:
```
GitHub → Repo → Settings → Secrets and variables → Actions
```
Add the following as separate secrets:
```
DOCKERHUB_USERNAME=<your-dockerhub-username>
```
```
DOCKERHUB_TOKEN=<your-dockerhub-access-token>
```
```
IMAGE_NAME=<your-dockerhub-username>/<your-image-name>
```
```
IMAGE_TAG_LATEST=<most-likely-package-name>
```
```
PREFIX_SHA=<most-likely-package-name>
```

On push to ```release```-branch GitHub Actions will install Python + uv, run tests with pytest, build the docker image and push it to dockerhub.

