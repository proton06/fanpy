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
        # print('args:', self.args)
        # print('argds:', self.argds)
        # print('method:', self.method)
        self.method(*self.args, **self.argds)


class OutDf(Outable):
    """
    pandas DataFrame または Series を出力します．

    parameters
    ----------
    

    """
    def __init__(self, obj, name, *args, **argds):
        self.obj = obj
        self.name = name
        self.argds = argds

    def output(self, path=''):
        self.argds['sep'] = ' '
        self.obj.to_csv(path / self.name, **self.argds)


class OutFig(ArgdsOutable):
    """
    matplotlib の Figure または Axes を出力します．このインスタンスを生成
    するときに matplotlib のデフォルトプロットは閉じられることに注意し
    てください.

    parameter
    ----------
    obj: matplotlib.figure.Figure または matplotlib.axes._subplots.Axes
        出力したいグラフオブジェクトを指定します
    name: str
        出力時のファイル名を指定します
    tight: bool
        出力時に余白を切り詰めるか指定します
    plt_close: bool
        出力時にデフォルトプロットを閉じるか指定します．True にすると
        matplotlib.pyplot.close が呼ばれます．
    """
    def __init__(self, obj, name, *args, tight=True,
                 plt_close=True, **argds):
        if isinstance(obj, matplotlib.axes._subplots.Axes):
            obj = obj.get_figure()
            
        if tight:
            argds['bbox_inches'] = 'tight'
        if plt_close:
            matplotlib.pyplot.close()
            
        super().__init__(obj.savefig, 'filename', name, *args, **argds)
        
