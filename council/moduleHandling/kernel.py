# -*- coding: utf-8 -*-
from glob import glob
import os
from pathlib import Path
import importlib
import json
from jsoncomment import JsonComment
import sys
import pprint
import types
import typing
from . import registry
pp = pprint.PrettyPrinter(indent=4)
MANIFEST_FILENAMES = ["__manifest__.json"]

#TODO Make manifest into class

#TODO Make module registry etc into classes

#TODO change to pathlib
def getManifest(path):
    basedir, subdirs, files = tuple(os.walk(path)) and tuple(os.walk(path))[0] or (None,(),())
    for manifestFilename in MANIFEST_FILENAMES:
        if manifestFilename in files:
            manifestPath = os.path.join(basedir,manifestFilename)
            with open(manifestPath) as jsonFile:
                parser = JsonComment(json)
                manifest = parser.load(jsonFile)
                manifest["_manifestFile"] = os.path.abspath(manifestPath)
                manifest["_initFile"] = os.path.abspath(os.path.join(path,"__init__.py"))
                manifest["_installable"] = None
                manifest["_loaded"] = False
                manifest["_path"] = path
                return manifest
    return False

#TODO change to pathlib
def isModule(path):
    if os.path.isdir(path):
        pythonFiles = [os.path.basename(filename) for filename in glob('%s/*.py' % path)]
        if '__init__.py' in pythonFiles:
            return True
    return False

def dependencySolver(module, resolvedModules, unresolvedModules):
   unresolvedModules.append(module)
   dependenciesNameList = module.get("depends")
   if dependenciesNameList:
       for dependencyName in dependenciesNameList:
           if dependencyName in registry.modules:
               dependency = registry.modules.get(dependencyName)
               if dependency not in resolvedModules:
                   if dependency in unresolvedModules:
                       raise Exception('Could not resolve module %s dependency %s' % (module["name"], dependency["name"]))
                   dependencySolver(dependency, resolvedModules, unresolvedModules)
                   if not dependency.get("_installable"):
                       module["_installable"] = False
           else:
               module["_installable"] = False
   module["_installable"] = True
   resolvedModules.append(module)
   unresolvedModules.remove(module)

def solveDependencies(modules):
    resolvedModules = []
    for module in modules:
        dependencySolver(module, resolvedModules, [])
    return resolvedModules

def getModules(path) -> list:
    path = Path(path).resolve() # Get a iterable Path-object and make it absolute
    modules = []
    print("Searching for modules in path %s" % path)
    subdirs = [p for p in path.iterdir() if p.is_dir()]
    print("Found %i subdirectories." % len(subdirs))
    for directory in subdirs:
        print("Checking directory %s" % directory)
        if isModule(directory):
            print("Found module in directory %s. Loading manifest..." % directory)
            manifest = getManifest(directory)
            if manifest:
                print("Success!")
                modules.append(manifest)
                registry.modules.update({manifest["name"]: manifest})
            else:
                print("Failure!")
    return modules

#TODO pythonName functions

def getCanonicalName(module):
    canonicalName = "council.%s" % module["name"]
    return canonicalName

def loadModules(modules):
    modules = solveDependencies(modules)
    for module in modules:
        canonicalName = getCanonicalName(module) #TODO Implement new finder an get rid of this function maybe?
        moduleSpec = importlib.machinery.ModuleSpec(canonicalName, loader, *, origin=None, loader_state=None, is_package=None)
        if module.get("_installable"):
            path = module["_path"].parent
            importlib.abc.FileLoader
            if path not in sys.path:
                print("Adding path %s to module search path." % path)
                sys.path.append(module["_path"].parent)
            else:
                print("Path %s is already in module searchpath." % path)
        else:
            print("Skipping module %s." % canonicalName)
    pp.pprint(registry.modules)
    importlib.invalidate_caches()
    
def getInstanceOf(module):
    return instance
