# -*- coding: utf-8 -*-
import council
import pprint as pp
import importlib
from pathlib import Path

if __name__ == "__main__":
    from .moduleHandling import kernel
    from .moduleHandling import registry
    internalAddonPath = Path(__file__).parent / 'addons'
    ADDON_PATHS = [internalAddonPath, "./addons/"]
    modules = []
    for path in ADDON_PATHS:
        try:
            modules += kernel.getModules(path)
        except FileNotFoundError as e:
            print("Error: %s" % e)
        print("Loading modules...")
    activeModules = [module for module in modules if module.get("active")]
    kernel.loadModules(activeModules)
    import council.log
    log = council.log.Log()
    log.warning("Test!")
