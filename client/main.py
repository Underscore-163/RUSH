import os
print(os.getcwd())
from frontend.app import App
from logger import get_main_logger


log=get_main_logger()

if __name__ == "__main__":
    log.info("=====Program Started=====")
    log.debug(os.getcwd())
    app=App()
    app.mainloop()
    log.info("=====Program Ended=====")
