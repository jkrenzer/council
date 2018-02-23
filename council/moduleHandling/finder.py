import importlib

class Finder(importlib.abc.MetaPathFinder):
    
    def find_spec(fullname, path, target=None)
        """
        Return importlib.machinery.ModuleSpec or None
        """
