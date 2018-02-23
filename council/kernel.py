# -*- coding: utf-8 -*-
from glob import glob
import os
import json
from jsoncomment import JsonComment
import sys
import pprint
import types
import typing
import council.registry as registry
pp = pprint.PrettyPrinter(indent=4)
MANIFEST_FILENAMES = ["__manifest__.json"]

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

def getModules(path: str) -> list:
    modules = []
    print("Searching for modules in path %s" % path)
    basedir, subdirs, files = tuple(os.walk(path)) and tuple(os.walk(path))[0] or (None,(),())
    for directory in subdirs:
        print("Checking directory %s" % directory)
        moduleDirectory = os.path.join(basedir,directory)
        if isModule(moduleDirectory):
            print("Found module in directory %s. Loading manifest..." % directory)
            manifest = getManifest(moduleDirectory)
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
        canonicalName = getCanonicalName(module)
        if canonicalName not in sys.modules and module.get("_installable"):
            moduleFile = module["_initFile"]
            newModule = types.ModuleType(canonicalName)
            newModule.__file__ = module["_initFile"]
            newModule.__path__ = [module["_path"]]
            newModule.__package__ = canonicalName
            sys.modules[canonicalName] = newModule
            pp.pprint(newModule)
            exec(open(moduleFile, 'rb').read(), newModule.__dict__)
            if canonicalName in sys.modules:
                print("Module %s is registered as %s" % (module["name"], canonicalName))
                registry.modules[module["name"]]["_loaded"] = True
            else:
                print("Module %s NOT loadable." % module["name"])
        else:
            print("Skipping module %s." % canonicalName)
    pp.pprint(registry.modules)

def getInstanceOf(module):
    return instance
