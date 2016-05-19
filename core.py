# -*- coding: utf-8 -*-
from pathlib import Path
from abc import ABCMeta, abstractmethod
from collections import Iterable
import re
from .outable import OutTab, OutFig, Outable
from lcs import lcs_from_list


class Analyzer(metaclass=ABCMeta):
    def __init__(self, keyword, group=False, out=''):
        """
        
        parameters
        ----------
        keyword : str
        group : boolean
        """
        self.keyword = keyword
        self.group = group
        self.out = out

        self.OutTab = OutTab
        self.OutFig = OutFig

    def execute(self, target='result', out='analyze'):
        target_path = Path(target)
        out_path = Path(out)
        self._sub_execute(target_path, out_path)

    def _sub_execute(self, target_path, out):
        target_filepaths = [filepath for filepath in target_path.iterdir()
                            if filepath.is_file()]
        for filepaths in self.categorize(target_filepaths):
            outs = self.analyze(filepaths)
            outs = outs if isinstance(outs, Iterable) else [outs]
            
            if outs:
                (out / self.out).mkdir(parents=True, exist_ok=True)
                
            for outable in outs:
                if not isinstance(outable, Outable):
                    raise TypeError('analyze() should return Outable'
                                    'or Outable array')
                fileid = self.solve_fileid([filepath.stem for filepath in filepaths] if isinstance(filepaths, list) else [filepaths.stem])
                outable.output(Path(str(out) + self.out), prefix=fileid)

        sub_dirs = [child for child in target_path.iterdir()
                    if child.is_dir()]
        for sub_dir in sub_dirs:
            self._sub_execute(sub_dir, out / sub_dir.name)

                
    def categorize(self, filepaths):
        matched_filepaths = self.match(filepaths)
        return self.grouping(matched_filepaths)

    
    def match(self, filepaths):
        return [(filepath, self.is_match(filepath)) for filepath
                in filepaths if self.is_match(filepath)]

    def is_match(self, filepath):
        name = filepath.stem
        return re.search(self.keyword, name)


    def grouping(self, filepaths):
        if not filepaths:
            return []
        
        if isinstance(self.group, bool):
            return self._grouping_by_bool(filepaths)
        elif isinstance(self.group, int):
            return self._grouping_by_int(filepaths)
        elif isinstance(self.group, str):
            return self._grouping_by_str(filepaths)
        else:
            raise TypeError('__init__() option group must be bool, '
                            'int or str type.')

    def _grouping_by_bool(self, filepaths):
        if self.group:
            return [[filepath[0] for filepath in filepaths]]
        else:
            return [filepath[0] for filepath in filepaths]

    def _grouping_by_int(self, filepaths):
        # TODO:
        raise NotImplementedError()
            
    def _grouping_by_str(self, filepaths):
        # TODO:
        raise NotImplementedError()


    def solve_fileid(self, filenames):
        lcs = lcs_from_list(filenames)
        return lcs if lcs[:1] != '_' else lcs[1:]

    
    @abstractmethod
    def analyze(self, filename):
        pass
