import sys, pathlib

def config_path() -> pathlib.Path:
    """
    Returns a parent directory path where persistent appl data can be stored.

    Linux: ~/.local/share
    MacOS: ~/Library/Application Support
    Windows: C:/Users/<USER>/AppData/Roaming
    """

    home = pathlib.Path.home()

    if sys.platform.startswith('win32'):
        return home / 'AppData/Roaming'
    elif sys.platform.startswith('linux'):
        return home / '.local/share'
    elif sys.platform.startswith('darwin'):
        return home / 'Library/Application Support'