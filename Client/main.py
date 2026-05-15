import time
import backend.logger as logger
import frontend.app as app

log=logger.get_main_logger()
log.info(f"starting at {time.time()}")
app.run()

