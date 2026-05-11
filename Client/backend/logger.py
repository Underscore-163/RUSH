import logging
from logging.config import dictConfig
import yaml
import os

def message_test():
    log.info("=====Testing logger=====")
    log.debug ("debug message")
    log.info ("info message")
    log.warning ("warning message")
    log.error ("error message")
    log.critical ("critical message")
    log.info("=====Test complete=====")

if __name__ == "__main__":
    os.chdir(os.getcwd().replace("server", ""))
with open("backend/log_config.yml") as file:
    log_config = yaml.safe_load(file)
dictConfig(log_config)

def get_main_logger():
    return logging.getLogger("main")

if __name__ == "__main__":
    log=get_main_logger()
    message_test()