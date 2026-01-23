import logging
from logging.config import dictConfig
import yaml
import os

def message_test():
    logger.debug ("debug message")
    logger.info ("info message")
    logger.warning ("warning message")
    logger.error ("error message")
    logger.critical ("critical message")

if __name__ == "__main__":
    os.chdir("data")
    print(os.getcwd())

print(os.getcwd())
with open("logs/log_config.yaml") as file:
    log_config = yaml.safe_load(file)
dictConfig(log_config)
logger=logging.getLogger("main")

if __name__ == "__main__":
    message_test()


