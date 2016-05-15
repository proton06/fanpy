# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod
import matplotlib


class Outable(metaclass=ABCMeta):
    @abstractmethod
    def output(self, path=''):
        pass


class ArgdsOutable(Outable):
    def __init__(self, method, name, argPath, *args, **argds):
        self.method = method
        self.name = name
        self.argPath = argPath
        self.argds = argds

    def output(self, path):
        if isinstance(self.argPath, str):
            self.argds[self.argPath] = path + name
        if isinstance(self.argPath, int):
            self.args.insert(self.argPath, path + self.name)

        self.method(*args, **argds)


class OutDf(Outable):
    def __init__(self, obj, name, **argds):
        self.obj = obj
        self.name = name
        self.argds = argds

    def output(self, path=''):
        self.argds['sep'] = ' '
        self.obj.to_csv(path / self.name, **self.argds)


class OutFig(Outable):
    def __init__(self, obj, name, **argds):
        if isinstance(obj, matplotlib.axes._subplots.Axes):
            obj = obj.get_figure()
        self.obj = obj
        self.name = name
        self.argds = argds
        matplotlib.pyplot.close()

    def output(self, path='', prefix=''):
        self.obj.savefig(str(path / (prefix + self.name)), **self.argds)
        matplotlib.pyplot.clf()
