from logger import get_main_logger
log=get_main_logger()

import json
import os


def load(filepath):
    if not os.path.isfile(filepath):
        log.error(f"Failed to load '{filepath}'; Not a file.")
        return None
    try:
        with open(filepath) as f:
            data = json.load(f)
        log.info(f"Loaded data from '{filepath}'.")
    except FileNotFoundError:
        log.error(f"Failed to load '{filepath}'; File not found.")
        data = None
    except PermissionError:
        log.error(f"Failed to load '{filepath}'; Permission Denied.")
        data = None
    except:
        log.error(f"Failed to load '{filepath}'; Something went wrong.")
    finally:
        return data

def save(filepath, data):
    with open(filepath, 'w') as f:
        json.dump(data, f)