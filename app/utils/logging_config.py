import logging
import sys


def configure_logging(app):
    """Server-side structured-ish logging. Errors always get full detail here even
    though clients only ever see the sanitized envelope message."""
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s in %(name)s: %(message)s"
    )
    handler.setFormatter(formatter)

    logger = logging.getLogger("univibe")
    logger.setLevel(logging.DEBUG if app.debug else logging.INFO)
    logger.addHandler(handler)
    logger.propagate = False

    app.logger.handlers = logger.handlers
    app.logger.setLevel(logger.level)
