# -*- coding: utf-8 -*-
import Council

import pprint as pp
import importlib
from pathlib import Path

if __name__ == "__main__":
    from Council.Modular import Kernel
    from Council.Modular import Registry
    Kernel.init()
    internalAddonPath = Path(__file__).parent / 'addons'
    ADDON_PATHS = [internalAddonPath, "./addons/"]
    modules = []
    for path in ADDON_PATHS:
        try:
            modules += Kernel.getModules(path)
        except FileNotFoundError as e:
            print("Error: %s" % e)
        print("Loading modules...")
    activeModules = [module for module in modules if module.get("active")]
    import Council.log
    log = Council.log.Log()
    log.warning("Test!")
