# -*- coding: utf-8 -*-
import council.registry as registry

class Watcher(type):
    def __init__(cls, name, bases, clsdict):
        if len(cls.mro()) > 2:
            registry.classes.update({cls._name:
                {
                    "type": cls,
                    "bases": bases,
                    #"dict": clsdict
                }
            })
        super(Watcher, cls).__init__(name, bases, clsdict)

class Class(metaclass=Watcher):
    pass
