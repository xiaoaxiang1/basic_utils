import time
from progressbar import ProgressBar

pb = ProgressBar("abcdefghighijklmnopqrstvuwxyz")

for i in ProgressBar(ProgressBar(iter(ProgressBar(range(10))))):
    for j in pb:
        #ProgressBar.print("hello world")
        ProgressBar.message(f"iterating... {i}, {j}")
        for k in ProgressBar(range(50)):
            #pb.message(f"iterating num: {k}")
            time.sleep(0.01)

