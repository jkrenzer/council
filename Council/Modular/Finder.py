import importlib

from . import Registry

class Finder(importlib.abc.MetaPathFinder):
    
  
    def find_spec(self, fullname, path, target=None):
        """
        Return importlib.machinery.ModuleSpec or None
        """
        manifest = Registry.modules.get(fullname, None)
        if manifest is not None:
            print("Module %s was found in plugins." % fullname)
            loader = importlib.machinery.SourceFileLoader(fullname, str(manifest['_initFile']))
            spec = importlib.machinery.ModuleSpec(fullname, loader, origin=str(manifest['_initFile']), is_package=True)
            spec.submodule_search_locations = [str(manifest['_path'])]
            return spec
        else:
            print("Module %s not found in plugins." % fullname)
            return None
