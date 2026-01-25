from logger import get_main_logger
log=get_main_logger()

import os
from frontend.app import App

if __name__ == "__main__":
    log.info("=====Program Started=====")
    log.info(f"working directory is {os.getcwd()}")
    app=App()
    app.mainloop()
    log.info("=====Program Ended=====")
