import time
import tqdm
from progressbar import ProgressBar

pb = ProgressBar("abcdefghighijklmnopqrstvuwxyz")
for i in ProgressBar(range(10)):
    for j in pb:
        time.sleep(0.05)
        #ProgressBar.print("hello world")
        ProgressBar.message(f"iterating... {i}, {j}")

for i in pb:
    pb.message("iterating")
    time.sleep(0.5)