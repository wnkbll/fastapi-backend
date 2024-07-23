from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent.parent
SRC_DIR = ROOT_DIR.joinpath("src")

DEV_ENV_PATH = ROOT_DIR.joinpath(".env")
PROD_ENV_PATH = ROOT_DIR.joinpath(".env.prod")
LOGGING_DIR = ROOT_DIR.joinpath("logs/")
