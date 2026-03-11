# FIX: Change imports from "python_project_blueprint" to packagename
from python_project_blueprint.cli.cli import main
from python_project_blueprint.api.api import api

if __name__ == "__main__":
    raise SystemExit(main())
