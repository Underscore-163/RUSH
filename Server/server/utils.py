import yaml
import os

async def load_config():
    with open("config/config.yml") as config_file:
        config = yaml.safe_load(config_file)
    return config

async def get_logger():
    from logger import get_main_logger
    log = get_main_logger()
    return log

async def go_up():
    if not os.getcwd()[-6:]=="Server":
        os.chdir("..")

async def part_setup():
    config = await load_config()
    log = await get_logger()
    return log, config

async def full_setup():
    await go_up()
    return await part_setup()



