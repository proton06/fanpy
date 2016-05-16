# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod
from pathlib import Path
import matplotlib
from pandas import Series, DataFrame

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


class OutTab(ArgdsOutable):
    """
    pandas の DataFrame または Series を出力します．

    parameters
    ----------
    obj : pandas.DataFrame または pandas.Series
        出力したいテーブルオブジェクトを指定します
    name : str
        出力時のファイル名を指定します
    """
    def __init__(self, obj, name, *args, **argds):
        if isinstance(obj, Series):
            path_arg_name = 'path'
        elif isinstance(obj, DataFrame):
            path_arg_name = 'path_or_buf'
        else:
            raise TypeError('obj should be pandas.Series or'
                            'pandas.DataFrame object')
        super().__init__(obj.to_csv, path_arg_name, name, *args, **argds)


class OutFig(ArgdsOutable):
    """
    matplotlib の Figure または Axes を出力します．このインスタンスを
    生成するときに matplotlib のデフォルトプロットは閉じられることに注
    意してください.

    parameter
    ----------
    obj : matplotlib.figure.Figure または matplotlib.axes._subplots.Axes
        出力したいグラフオブジェクトを指定します
    name : str
        出力時のファイル名を指定します
    tight : bool
        出力時に余白を切り詰めるか指定します
    plt_close : bool
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
        
