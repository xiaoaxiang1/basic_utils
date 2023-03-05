import time
import tqdm
from progressbar import ProgressBar

pb = ProgressBar("abcdefghigklmnopqrstuvwxyz")
for i in ProgressBar("1234567890"):
    for j in pb:
        time.sleep(0.1)
        ProgressBar.message(f"iterating... {i}, {j}")

for i in pb:
    pb.message("iterating")
    time.sleep(0.5)