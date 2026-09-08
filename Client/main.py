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
        ErrorPopup(traceback.format_exc())
    except:
        FatalErrorPopup("RUSH_ERROR_IN_HANDLER")



