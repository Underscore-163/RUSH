import os
import logging

os.chdir(os.getcwd().replace("debug_scripts","data"))
logging.basicConfig(filename="logs/main.log",
                    format = "%(asctime)s - %(levelname)s - %(message)s",
                    level=logging.DEBUG)

with open("logs/main.log","w") as f:
    f.write("")
logging.info("logs cleared")