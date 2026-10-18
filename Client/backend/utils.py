import platform
import subprocess
import os

def open_file(filepath:str):
    # Source - https://stackoverflow.com/a/435669
    # Posted by Nick, modified by community. See post 'Timeline' for change history
    # Retrieved 2026-08-13, License - CC BY-SA 4.0
    # (Modified for this codebase)
    if platform.system() == 'Darwin':  # macOS
        subprocess.call(('open', filepath))
    elif platform.system() == 'Windows':  # Windows
        os.startfile(filepath)
    else:  # linux variants
        subprocess.call(('xdg-open', filepath))