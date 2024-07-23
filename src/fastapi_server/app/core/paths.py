from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent.parent.parent.parent
SRC_DIR = ROOT_DIR.joinpath("src")
LOGGING_DIR = ROOT_DIR.joinpath("logs")

APP_DIR = SRC_DIR.joinpath("fastapi_server/app")
ENV_PATH = SRC_DIR.joinpath(".env")
