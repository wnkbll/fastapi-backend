import json
import atexit
import logging
import pathlib
import logging.config
import logging.handlers

from functools import lru_cache


class Logger:
    def __init__(self, config_file: str = "config.json"):
        self._logger: logging.Logger = logging.getLogger("news_app")
        self._path: str = config_file

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
