from warnings import warn
import time
import backend.logger as logger
import frontend.app as app
from performance_timer import PerformanceTimer
warn("\n\n---THIS COMMIT IS NON-FUNCTIONAL AND HAS BEEN COMMITED TO COME BACK TO LATER---\n\n")
performance_timer = PerformanceTimer()

performance_timer.start()
log=logger.get_main_logger()
log.info(f"starting at {time.time()}")
if __name__ == "__main__":
    app.run()

