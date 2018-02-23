# -*- coding: utf-8 -*-
import council
import pprint as pp
import importlib
if __name__ == "__main__":
    import council.kernel as kernel
    ADDON_PATHS = ["./council/modules"]
    modules = []
    for path in ADDON_PATHS:
        print("Searching for modules in path %s" % path)
        modules += kernel.getModules(path)
        print("Loading modules...")
    activeModules = [module for module in modules if module.get("active")]
    kernel.loadModules(activeModules)
    Log = council.registry.classes["log"]["type"]()
    Log.warning("Test!")
