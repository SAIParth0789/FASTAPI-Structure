
import logging
from logging.config import dictConfig

from project_name.config import DevConfig, config


def obfuscated(email: str, obfuscated_length: int) -> str:
    characters = email[:obfuscated_length]
    first, last = email.split("@")
    return characters + ("*" * (len(first) - obfuscated_length)) + "@" + last


class EmailObfuscationFilter(logging.Filter):
    def __init__(self, name: str = "", obfuscated_length: int = 2) -> None:
        super().__init__()
        self.obfuscated_length = obfuscated_length

    def filter(self, record: logging.LogRecord) -> bool:
        if "email" in record.__dict__:
            record.email = obfuscated(record.email, self.obfuscated_length)
        return True


def configure_logging() -> None:
    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "filters": {
                "correlation_id": {
                    "()": "asgi_correlation_id.CorrelationIdFilter",
                    "uuid_length": 8 if isinstance(config, DevConfig) else 32,
                    "default_value": "-"
                },
                "email_obfuscation": {
                    "()": EmailObfuscationFilter,
                    "obfuscated_length": 2 if isinstance(config, DevConfig) else 0,
                }
            },
            "formatters": {
                "console": {
                    "class": "logging.Formatter",
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                    "format": "(%(correlation_id)s) %(name)s:%(lineno)d - %(message)s"
                },
                "file": {
                    # "class": "logging.Formatter", # for normal formatter
                    "class": "pythonjsonlogger.jsonlogger.JsonFormatter",  # for json formatter
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                    # "format": "%(asctime)s.%(msecs)03dZ | %(levelname)-8s | [%(correlation_id)s] %(name)s:%(lineno)d - %(message)s" # for normal formatter
                    "format": "%(asctime)s %(msecs)03dZ %(levelname)-8s %(correlation_id)s %(name)s %(lineno)d %(message)s"
                    # for json formatter
                }
            },
            "handlers": {
                "default": {
                    "class": 'rich.logging.RichHandler',
                    "level": "DEBUG",
                    "formatter": "console",
                    "filters": ["correlation_id", "email_obfuscation"]
                },
                "rotating_file": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "level": "DEBUG",
                    "formatter": "file",
                    "filename": "logs/projectapi.log",
                    "maxBytes": 1024 * 1024 * 1,  # 1MB
                    "backupCount": 5,
                    "encoding": "utf8",
                    "filters": ["correlation_id", "email_obfuscation"]
                },
                "logtail": {
                    "class": "logtail.LogtailHandler",
                    "level": "DEBUG",
                    "formatter": "console",
                    "filters": ["correlation_id", "email_obfuscation"],
                    "source_token": config.LOGTAIL_API_KEY
                }
            },
            "loggers": {
                "uvicorn": {"handlers": ["default", "rotating_file"], "level": "INFO"},
                "projectapi": {
                    "handlers": ["default", "rotating_file", "logtail"],
                    "level": "DEBUG" if isinstance(config, DevConfig) else "INFO",
                    "propagate": False
                },
                "databases": {"handlers": ["default"], "level": "WARNING"},
                "aiosqlite": {"handlers": ["default"], "level": "WARNING"}
            }
        }
    )
