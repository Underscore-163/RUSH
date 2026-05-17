import time
import backend.logger as logger
import frontend.app as app
from performance_timer import PerformanceTimer

performance_timer = PerformanceTimer()

performance_timer.start()
log=logger.get_main_logger()
log.info(f"starting at {time.time()}")
app.run()

