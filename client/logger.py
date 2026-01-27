import logging
from logging.config import dictConfig
import yaml

def message_test():
    log.debug("=====Testing logger=====")
    log.debug ("debug message")
    log.info ("info message")
    log.warning ("warning message")
    log.error ("error message")
    log.critical ("critical message")
    log.debug("=====Test complete=====")


with open("data/logs/log_config.yaml") as file:
    log_config = yaml.safe_load(file)
dictConfig(log_config)

def get_main_logger():
    return logging.getLogger("main")

if __name__ == "__main__":
    log=get_main_logger()
    message_test()


