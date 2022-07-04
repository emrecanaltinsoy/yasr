import logging

logger = logging.getLogger("yasr")
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)
