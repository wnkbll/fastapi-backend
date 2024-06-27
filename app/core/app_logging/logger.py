import json
import atexit
import logging
import pathlib
import logging.config
import logging.handlers

from functools import lru_cache


class Logger:
    def __init__(self, config_file: str = "../logger_config.json", log_dir: str = "../logs"):
        self._logger: logging.Logger = logging.getLogger("news_app")
        self._path: str = config_file
        self._log_dir: str = log_dir

        self.create_log_directory()

    def create_log_directory(self) -> None:
        log_dir = pathlib.Path(self._log_dir)

        if not log_dir.exists():
            log_dir.mkdir()

    def setup(self) -> None:
        config_file = pathlib.Path(self._path)

        with open(config_file) as f_in:
            config = json.load(f_in)

        logging.config.dictConfig(config)

        queue_handler = logging.getHandlerByName("queue_handler")
        if queue_handler is not None:
            queue_handler.listener.start()
            atexit.register(queue_handler.listener.stop)

    @property
    @lru_cache
    def logger(self) -> logging.Logger:
        self.setup()
        return self._logger
