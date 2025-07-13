import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter(
    fmt='{asctime} | levelname={levelname} | {module}:{funcName}:{lineno} | {message}',
    style='{'
)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)