import backend.logger as logger
import frontend.app as app
log=logger.get_main_logger()
log.info("starting")
app.run()

