import logging
from logging.config import dictConfig
import yaml
import os

def message_test():
    logger.debug("=====Testing logger=====")
    logger.debug ("debug message")
    logger.info ("info message")
    logger.warning ("warning message")
    logger.error ("error message")
    logger.critical ("critical message")
    logger.debug("=====Test complete=====")



print(os.getcwd())
with open("data/logs/log_config.yaml") as file:
    log_config = yaml.safe_load(file)
dictConfig(log_config)

def get_main_logger():
    return logging.getLogger("main")

if __name__ == "__main__":
    logger=logging.getLogger("main")
    message_test()


