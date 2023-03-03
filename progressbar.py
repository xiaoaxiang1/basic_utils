import time
import platform

def iter_count(file_name):
    from itertools import (takewhile, repeat)
    buffer = 1024 * 1024
    with open(file_name) as f:
        buf_gen = takewhile(lambda x: x, (f.read(buffer) for _ in repeat(None)))
        return sum(buf.count('\n') for buf in buf_gen)

class ProgressBar:
    ITERATOR_LIST = []
    def __init__(self, iterator=None, describution="", bar_len=20, reprint=False, line_feed=False):
        self.__iterator     = iterator
        self.__desp         = describution
        self.__bar_len      = bar_len
        self.__reprint      = reprint
        self.__end          = "\n" if line_feed else "\r"

        self.__total        = self.__get_length(iterator)
        self.__cnt          = 0
        self.__msg          = ''


    def __iter__(self):
        return ProgressBar(self.__iterator)

    def __next__(self):
        try:
            iter_tgt = next(self.__iterator)
        except StopIteration:
            self.update()
            raise StopIteration
        else:
            self.update()
            return iter_tgt

    def __call__(self, iterator=None):
        if not iterator:
            return ProgressBar(self.__iterator)
        return ProgressBar(iterator)
    
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



