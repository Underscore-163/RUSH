import os
import logging

os.chdir(os.getcwd().replace("debug_scripts","data"))
logging.basicConfig(filename="logs/main.log",
                    format = "%(asctime)s - %(filename)s - %(levelname)s - %(message)s (logged from %(funcName)s, line %(lineno)d)",
                    level = logging.DEBUG)

with open("logs/main.log","w") as f:
    f.write("")
logging.info("logs cleared")