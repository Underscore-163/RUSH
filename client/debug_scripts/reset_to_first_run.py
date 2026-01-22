import os
import logging

os.chdir(os.getcwd().replace("debug_scripts","data"))
logging.basicConfig(filename="logs/main.log",
                    format = "%(asctime)s - %(levelname)s - %(message)s",
                    level=logging.DEBUG)

open("first_session","w").close()
logging.debug("reset to first session")
logging.error("error message")
