import time
import traceback
from tkinter import messagebox
import backend.logger as logger
import frontend.app as app
from Client.frontend.widgets.error_popup import ErrorPopup, FatalErrorPopup


log=logger.get_main_logger()
log.info(f"starting at {time.time()}")
try:
    app.run()
except Exception as e:
    try:
        log.error(traceback.format_exc())
        FatalErrorPopup(error_code="RUSH_STARTUP_ERROR")
        ErrorPopup(traceback.format_exc(),parent_window=None)
    except Exception as e:
        FatalErrorPopup()



