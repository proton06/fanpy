# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod
from pathlib import Path
import matplotlib


class Outable(metaclass=ABCMeta):
    @abstractmethod
    def output(self, path=''):
        pass


class ArgdsOutable(Outable):
    def __init__(self, method, path_arg_name, name, *args, **argds):
        self.method = method
        self.path_arg_name = path_arg_name
        self.name = name
        self.args = args
        self.argds = argds

    def output(self, path=Path(), prefix=''):
        self.argds[self.path_arg_name] = str(path / (prefix + self.name))
        self.method(*self.args, **self.argds)


class OutDf(Outable):
    def __init__(self, obj, name, **argds):
        self.obj = obj
        self.name = name
        self.argds = argds

    def output(self, path=''):
        self.argds['sep'] = ' '
        self.obj.to_csv(path / self.name, **self.argds)


class OutFig(ArgdsOutable):
    """
    matplotlib Figure または Axes を出力します．このインスタンスを生成
    するときにデフォルトプロットは閉じられることに注意してください.

    parameter
    ----------
    obj: matplotlib.figure.Figure または matplotlib.axes._subplots.Axes
        出力したいグラフオブジェクトを指定します

    name: str
        出力時のファイル名を指定します

    tight: bool
        出力時に余白を切り詰めるか指定します
    """
    def __init__(self, obj, name, *args, tight=True, **argds):
        if isinstance(obj, matplotlib.axes._subplots.Axes):
            obj = obj.get_figure()
            
        if tight:
            argds['bbox_inches'] = 'tight'
            
        super().__init__(matplotlib.figure.Figure.savefig, 'filename',
                         name, obj, *args, **argds)
        matplotlib.pyplot.close()
