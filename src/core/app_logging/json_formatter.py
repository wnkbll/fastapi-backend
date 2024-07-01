import datetime
import json
import logging

LOG_RECORD_BUILTIN_ATTRS = {
    "args",
    "asctime",
    "created",
    "exc_info",
    "exc_text",
    "filename",
    "funcName",
    "levelname",
    "levelno",
    "lineno",
    "module",
    "msecs",
    "message",
    "msg",
    "name",
    "pathname",
    "process",
    "processName",
    "relativeCreated",
    "stack_info",
    "thread",
    "threadName",
    "taskName",
}


class JSONFormatter(logging.Formatter):
    def __init__(self, *, format_keys: dict[str, str] | None = None):
        super().__init__()

        self.format_keys = format_keys if format_keys is not None else {}

    def format(self, record: logging.LogRecord) -> str:
        message = self._prepare_log_dict(record)
        return json.dumps(message, default=str)

    def _prepare_log_dict(self, record: logging.LogRecord) -> dict[str, any]:
        required_fields: dict[str, any] = {
            "message": record.getMessage(),
            "timestamp": datetime.datetime.fromtimestamp(
                record.created, tz=datetime.timezone.utc
            ).isoformat(),
        }

        if record.exc_info is not None:
            required_fields["exc_info"] = self.formatException(record.exc_info)

        if record.stack_info is not None:
            required_fields["stack_info"] = self.formatStack(record.stack_info)

        message: dict[str, any] = {
            key: value
            if (value := required_fields.pop(val, None)) is not None
            else getattr(record, val)
            for key, val in self.format_keys.items()
        }

        return message
