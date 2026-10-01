"""CLI logging, without changing an embedding application's root logger."""

import logging

app_logger = logging.getLogger("djhx_blogger")
app_logger.addHandler(logging.NullHandler())


def log_init(verbose: bool = False) -> None:
    app_logger.handlers.clear()
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
    app_logger.addHandler(handler)
    app_logger.setLevel(logging.DEBUG if verbose else logging.INFO)
    app_logger.propagate = False
