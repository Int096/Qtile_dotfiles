import os
from libqtile import hook

def set_environment():
    os.environ["OBSIDIAN_USE_WAYLAND"] = "1"


set_environment()
