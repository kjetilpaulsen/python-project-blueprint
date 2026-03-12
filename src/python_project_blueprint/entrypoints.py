import sys

import uvicorn

from python_project_blueprint.cli.cli import cli
from python_project_blueprint.identity import IDENTITY

def cli_main(argv: list[str]) -> int:
    return cli(argv)

def api_main(argv: list[str]) -> int:
    host = "127.0.0.1"
    port = 8001
    reload = False

    i = 0
    while i < len(argv):
        arg = argv[i]

        if arg == "--reload":
            reload = True
            i += 1
            continue

        if arg == "--host":
            i += 1
            host = argv[i]
            i += 1
            continue

        if arg == "--port":
            i += 1
            port = int(argv[i])
            i += 1
            continue

        print(f"Unknown api arg {arg}", file=sys.stderr)
        return 2

    uvicorn.run(
        f"{IDENTITY.package_name}.api.api:api",
        host=host,
        port=port,
        reload=reload,
    )
    return 0

