import logging


def get_logger():
    logger = logging.getLogger("logger")
    logger.setLevel(logging.INFO)

    log_file_path = "/var/log/monit/monit.log"
    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )

    file_handler = logging.FileHandler(log_file_path)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger


def write_log_message(message):
    logger = get_logger()
    logger.info(message)
