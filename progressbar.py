import time

def iter_count(file_name):
    from itertools import (takewhile, repeat)
    buffer = 1024 * 1024
    with open(file_name) as f:
        buf_gen = takewhile(lambda x: x, (f.read(buffer) for _ in repeat(None)))
        return sum(buf.count('\n') for buf in buf_gen)

class ProgressBarIter:
    __attr           = {"descrip": '', "bar_len": 30, "reprint": True, "linefeed": False, "message": ''}
    __iter_list      = []
    # attr can set
    __descrip        = __attr["descrip"]
    __bar_len        = __attr["bar_len"]
    __reprint        = __attr["reprint"]
    __linefeed       = __attr["linefeed"]
    __end            = ''
    __message        = __attr["message"]
    # internal attr
    #__itered_stage   = [True, True]
    __cnt            = []  # cnt[1] default is 0, when init stage1, set it to -1
    __cnt_rec        = []
    __cnt_val        = 0
    __total          = []  # total[1] default is 1, when init stage1, set it to len(stage1)
    __total_rec      = []
    __total_val      = 1
    __bar_str        = ''
    # time
    __time_start     = -1
    __time_rec       = -1
    __time_str       = ''

    def __init__(self, iter_obj, **kwargs):
        
        iterator = iter(iter_obj)
        if not isinstance(iterator, ProgressBarIter):
            ProgressBarIter.__iter_list.append(iterator)
            ProgressBarIter.__cnt.append(-1)
            ProgressBarIter.__total.append(max(0, self.__get_length(iter_obj)))
            ProgressBarIter.__set_attr(**kwargs)

    def __next__(self):
        try:
            ProgressBarIter.__update()
            return next(ProgressBarIter.__iter_list[-1])
        except Exception as e:
            ProgressBarIter.__reset()
            raise e
    
    @classmethod
    def __reset(cls):
        cls.__iter_list.pop()
        cls.__cnt.pop()
        cls.__total.pop()
        if not cls.__iter_list:
            cls.__set_attr(**cls.__attr)
            cls.__cnt_rec    = []
            cls.__cnt_val    = 0
            cls.__total_rec  = []
            cls.__total_val  = 1
            cls.__bar_str    = ''
            cls.__time_start = -1
            cls.__time_rec   = -1
            cls.__time_str   = ''
            None if cls.__linefeed else print()
    
    @staticmethod
    def __time2str(t):
        t = round(t)
        if t == -1:
            tstr = '--'
        elif t > 3600:
            h = t // 3600
            m = (t % 3600) // 60
            s = t % 60
            tstr = '{}h{:d}m{:d}s'.format(h, m, s)
        elif t > 60:
            m = t // 60
            s = t % 60
            tstr = '{:d}m{:d}s'.format(m, s)
        else:
            s = t
            tstr = '{:d}s'.format(s)
        return tstr
    
    @classmethod
    def __time_update(cls, cnt, total):
        if cls.__time_start == -1:
            cls.__time_start = time.time()
            cls.__time_rec   = cls.__time_start
            cls.__time_str   = f" [TS:{cls.__time2str(0)}|ETA:{cls.__time2str(-1)}] "
            return True
        time_curr  = time.time()
        if time_curr - cls.__time_rec > 0.5:
            total, cnt        = (0, 1) if cnt <= 0 else (total, cnt)
            time_spend        = time_curr - cls.__time_start
            time_eta          = -1 if cnt == 0 else time_spend * (total/cnt - 1)
            cls.__time_str    = f" [TS:{cls.__time2str(time_spend)}|ETA:{cls.__time2str(time_eta)}] "
            cls.__time_rec    = time.time()
            return True
        return False
    
    @classmethod
    def __update(cls):
        if cls.__total_rec != cls.__total or cls.__cnt_rec != cls.__cnt:
            cls.__cnt[-1] += 1
            cls.__cnt_val   = 0
            cls.__total_val = 1
            
            for c, t in zip(cls.__cnt[::-1], cls.__total[::-1]):
                cls.__cnt_val   = c * cls.__total_val + cls.__cnt_val
                cls.__total_val = t * cls.__total_val
                
            cls.__cnt_rec   = cls.__cnt.copy()
            cls.__total_rec = cls.__total.copy()
        else:
            cls.__cnt[-1]     += 1
            cls.__cnt_val     += 1
            cls.__cnt_rec[-1]  = cls.__cnt[-1]
                    
        cnt               = min(cls.__cnt_val, cls.__total_val)
        total             = cls.__total_val
        if total == 0:
            return

        time_updated      = cls.__time_update(cnt, total)
        time_str          = cls.__time_str

        pb_len            = [0, 0]
        pb_len[0]         = round(cnt / total * cls.__bar_len)
        pb_len[1]         = round(cls.__cnt[-1] / cls.__total[-1] * pb_len[0]) if len(cls.__iter_list) > 1 else pb_len[0]

        

        #if (stage+1) == len(cls.__iter_list) and (   cls.__reprint 
        if                                        (  cls.__reprint   
                                                  or time_updated
                                                  or cnt == total):
            
            pct_str   = "{:d}% ({}/{})".format(round(cnt/total*100), cls.__cnt[0], cls.__total[0])
            bar_str   = "\r" + cls.__descrip + '|' + '#' * pb_len[1] + \
                        '>'  * (pb_len[0] - pb_len[1]) + \
                        '-'  * (cls.__bar_len - pb_len[0]) + '|' + \
                        pct_str + time_str + cls.__message
            
            bs_len    = len(bar_str)
            if len(cls.__bar_str) > bs_len:
                bar_str = bar_str + ' ' * (len(cls.__bar_str) - bs_len)
            cls.__bar_str     = bar_str[:bs_len]
            
            print(bar_str, end=cls.__end)
            
    
    @classmethod
    def __set_attr(cls, **kwargs):
        cls.__descrip   = kwargs["descrip"]  if "descrip"  in kwargs.keys() else cls.__descrip
        cls.__bar_len   = kwargs["bar_len"]  if "bar_len"  in kwargs.keys() else cls.__bar_len
        cls.__reprint   = kwargs["reprint"]  if "reprint"  in kwargs.keys() else cls.__reprint
        cls.__message   = kwargs["message"]  if "message"  in kwargs.keys() else cls.__message
        cls.__linefeed = kwargs["linefeed"] if "linefeed" in kwargs.keys() else cls.__linefeed
        cls.__end       = '\n' if cls.__linefeed else ''
    
    @classmethod
    def message(cls, message):
        cls.__set_attr(message=str(message))
    
    @classmethod
    def print(cls, *args, **kwargs):
        None if cls.__linefeed else print("\r" + ' ' * len(cls.__bar_str) + "\r", end='')
        print(*args, **kwargs)
        None if cls.__linefeed else print(cls.__bar_str, end=cls.__end)
    
    def __get_length(self, obj):
        if hasattr(obj, "__len__"):
            return len(obj)
        if self.isfilelike(obj):
            return iter_count(obj)
        raise Exception(f"iterator object {obj} has no attribute '__len__'")
    
    @staticmethod
    def isfilelike(f):
        try:
            if isinstance(getattr(f, "read"), collections.Callable) \
                    and isinstance(getattr(f, "write"), collections.Callable) \
                            and isinstance(getattr(f, "close"), collections.Callable):
                return True
        except AttributeError:
            pass
        return False


class ProgressBar:
    def __init__(self, iter_obj=None, **kwargs):
        self.__iter_obj = iter_obj
        self.__kwargs   = kwargs

    def __iter__(self):
        if isinstance(self.__iter_obj, ProgressBar):
            return iter(self.__iter_obj)
        if isinstance(self.__iter_obj, ProgressBarIter):
            return self.__iter_obj
        return ProgressBarIter(self.__iter_obj, **self.__kwargs)

    def __call__(self, iter_obj=None, **kwargs):
        self.__iter_obj = iter_obj if iter_obj and iter_obj != self else self.__iter_obj
        for k, v in kwargs.items():
            self.__kwargs[k] = v
        return self
    
    def __len__(self):
        return len(self.__iter_obj)
    
    def set(self, **kwargs):
        for k, v in kwargs.items():
            self.__kwargs[k] = v
        return self
    
    @staticmethod
    def message(message):
        return ProgressBarIter.message(message)
    
    @staticmethod
    def print(*args, **kwargs):
        return ProgressBarIter.print(*args, **kwargs)