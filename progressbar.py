import time
import platform

# todo: 时间
# todo: print功能
# todo: half strbar 1/4 3/4黑块
# todo: 空格覆盖多余的字符

def iter_count(file_name):
    from itertools import (takewhile, repeat)
    buffer = 1024 * 1024
    with open(file_name) as f:
        buf_gen = takewhile(lambda x: x, (f.read(buffer) for _ in repeat(None)))
        return sum(buf.count('\n') for buf in buf_gen)

class ProgressBarIter:
    __iterator_list = []
    __message        = ""
    __itered_stage   = [True, True]
    __descrip        = ''
    __bar_len        = 20
    __reprint        = False
    __end            = ''
    __cnt            = [0, 0]
    __total          = [1, 1]
    __pb_len         = [-1, -1]

    def __init__(self, iter_obj, **kwargs):
        if len(ProgressBarIter.__iterator_list) == 2:
            raise RecursionError("max progress bar recursion depth is 2")
        
        ProgressBarIter.__iterator_list.append(iter(iter_obj))
        
        self.__stage = len(ProgressBarIter.__iterator_list)
        ProgressBarIter.__itered_stage[self.__stage-1] = False
        ProgressBarIter.__total[self.__stage-1]  = self.__get_length(iter_obj)
        ProgressBarIter.__total[0] = ProgressBarIter.__total[0] * ProgressBarIter.__total[1]
        ProgressBarIter.set_attr(**kwargs)

    def __next__(self):
        ProgressBarIter.__update(self.__stage)
        try:
            next_tgt = next(ProgressBarIter.__iterator_list[self.__stage-1])
        except StopIteration:
            ProgressBarIter.__itered_stage[self.__stage-1] = True
            if all(ProgressBarIter.__itered_state):
                ProgressBarIter.__iterator_list = []
            raise StopIteration
        else:
            return next_tgt
    
    @classmethod
    def __update(cls, stage):
        cnt       = cls.__cnt[0] * cls.__total[1] + cls.__cnt[1]
        total     = cls.__total[0]
        pb_len    = cls.__pb_len
        pb_len[0] = round(cnt / total) * cls.__bar_len
        pb_len[1] = round(cls.__cnt[1] / cls.__total[1]) * pb_len[0]

        bar_str   = '\r' + cls.__descrip + '0' * pb_len[1] + \
                     '0' * (pb_len[0] - pb_len[1]) + \
                     ' ' * (cls.__bar_len - pb_len[0]) + \
                     cls.__message
            
        if stage == len(cls.__iterator_list) and (   cls.__reprint 
                                                  or pb_len != cls.__pb_len
                                                  or cnt == total):
            print(bar_str, end=cls.__end)

        cls.__cnt[stage-1] += cls.__cnt[stage-1]
        cls.__pb_len        = pb_len
    
    @classmethod
    def set_attr(cls, descrip='', bar_len=20, reprint=False, line_feed=False):
        cls.__descrip   = descrip
        cls.__bar_len   = bar_len
        cls.__reprint   = reprint
        cls.__end       = '\n' if line_feed else ''
    
    @staticmethod
    def __get_length(obj):
        if hasattr(obj, "__len__"):
            return len(obj)
        if isinstance(obj, file):
            return iter_count(obj)
        raise Exception(f"iterator object {obj} has no attribute '__len__'")




class ProgressBar:
    def __init__(self, iter_obj=None, descrip='', bar_len=20, reprint=False, line_feed=False):
        self.__iter_obj     = iter_obj
        self.__descrip      = descrip
        self.__bar_len      = bar_len
        self.__reprint      = reprint
        self.__line_feed    = line_feed

    def __iter__(self):
        return ProgressBarIter(self.__iter_obj, 
                               descrip=self.__descrip,
                               bar_len=self.__bar_len,
                               reprint=self.__reprint,
                               line_feed=self.__line_feed)

    def __call__(self, iter_obj=None):
        if iter_obj:
            self.__iter_obj = iter_obj
        return self
    
    @staticmethod
    def __get_length(obj):
        if hasattr(obj, "__len__"):
            return len(obj)
        if isinstance(obj, file):
            return iter_count(obj)
        raise Exception(f"iterator object {obj} has no attribute '__len__'")

    def __print_bar(self):
        
        pass

    def message(self, message:str):
        self.__msg = message
    
    def update(self, message:str=''):
        if message:
            self.__msg = message


        if self.__reprint or 
    
    def subprocess(self, cnt, total):



