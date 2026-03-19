import asyncio
import utils
log,config=asyncio.run(utils.full_setup())
import api

log.info("====Server start====")

if __name__ == "__main__":
    api.start_server()

