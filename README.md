# python-project-blueprint

This repo was originally intended to be kept privat, so I am in the process of rewriting this README.md. The README.md should be updated by March 23, 2026.

A blueprint for creating python projects. Copy the contents of this repo into a new python project, and use this as a starting point for your project. 

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
- Python >= 3.x
- uv

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
