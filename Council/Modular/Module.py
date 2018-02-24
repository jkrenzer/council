# -*- coding: utf-8 -*-
from . import Registry

class Watcher(type):
    def __init__(cls, name, bases, clsdict):
        if len(cls.mro()) > 2:
            Registry.classes.update({cls._name:
                {
                    "type": cls,
                    "bases": bases,
                    #"dict": clsdict
                }
            })
        super(Watcher, cls).__init__(name, bases, clsdict)

class Class(metaclass=Watcher):
    pass
