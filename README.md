# python-project-blueprint

### Description

A modular Python project template for building CLI and API applications with a shared core, structured runtime configuration, and production-ready tooling (logging, testing, Docker, CI/CD).

### What this is

This repository is a **starting point**, not a finished application.

It provides:
- A clean architecture for command-driven applications
- A unified backend usable from both CLI and HTTP API
- A production-ready foundation (logging, config, Docker, CI)

## Table of contents:
 - Quick start
 - Features
 - Architecture
 - Installation
   - Requirements
   - Setup
   - Usage
   - Testing
 - Docker & Github Actions
   - Local docker usage
   - GitHub Actions setup

## Quick Start

```bash
git clone ...
cd python-project-blueprint
uv sync
uv run python -m python_project_blueprint cli version
```

## Features

- Dual entrypoints: CLI and FastAPI (HTTP API)
- Command → Handler → Event pipeline for decoupled execution and output
- Unified application core reused across CLI and API frontends
- Structured runtime configuration (overrides → env → config → defaults)
- XDG-compliant directory layout (data, config, state, cache, tmp, logs)
- Flexible logging system (file, console, stderr with configurable levels)
- Pydantic-based settings management with validation
- Typed command and event system for predictable flow and extensibility
- Test suite for core components (pytest + coverage support)
- Docker support (Dockerfile + docker-compose for local execution)
- CI/CD pipeline (GitHub Actions: test → build → push Docker image)
- Designed for extensibility (easy to add new commands, handlers, frontends)

## Architecture
- To come

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
```bash
source .venv/bin/activate
```
### Usage
To see the list of available commands:

```bash
uv run python -m python_project_blueprint cli -h
```
You now have a couple of options for how to run the app. Since this is a foundation for other projects, it only has one command, ```version```, with one optional command ```--uppercase```. It will return an event that contains the version of the app and the "v" infront of the version is either uppercase or lowercase.

To test in CLI mode:
```bash
uv run python -m python_project_blueprint cli version
```

To test in API mode:
```bash
uv run python -m python_project_blueprint api
```
Or with spesific host, port and reload:
```bash
uv run python -m python_project_blueprint api \
  --host 127.0.0.1 \
  --port 8001 \
  --reload
```
This can then be tested with curl like so:
```bash
curl http://127.0.0.1:8001/health
```
And the ```version``` can be tested by running the command:
```bash
curl -X POST http://127.0.0.1:8001/run \
  -H "Content-Type: application/json" \
  -d '{
    "commands": [
      { "name": "version", "options": {} }
    ]
  }'
```
If you want the app to build a config file in ```~/.config/python-project-blueprint/python_project_blueprint.conf```:
```bash
uv run python -m python_project_blueprint cli --build-config
```
### Testing
The app also supports testing with pytest:
```bash
uv run pytest
```
or with coverage:
```bash
uv run pytest -V --cov=python_project_blueprint --cov-report=term-missing
```

## Docker & GitHub Actions Setup

### Overview

- **Docker**: Used to build and run the API locally
- **Docker Compose**: Runs the API container (no database required)
- **GitHub Actions**: Runs tests and builds/pushes Docker images on `release` branch

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
```bash
docker compose up --build
```
And stop it like so:
```bash
docker compose down
```
Test the API entrypoint while running the container like so:
```bash
curl http://127.0.0.1:8010/health
```

## Github Actions usage

### 1. Setup secrets in your repo
Navigate to secrets:
```bash
GitHub → Repo → Settings → Secrets and variables → Actions
```
Add the following as separate secrets:
```env
DOCKERHUB_USERNAME=<your-dockerhub-username>
```
```env
DOCKERHUB_TOKEN=<your-dockerhub-access-token>
```
```env
IMAGE_NAME=<your-dockerhub-username>/<your-image-name>
```
```env
IMAGE_TAG_LATEST=<most-likely-package-name>
```
```env
PREFIX_SHA=<most-likely-package-name>
```

On push to ```release```-branch GitHub Actions will install Python + uv, run tests with pytest, build the docker image and push it to dockerhub.

