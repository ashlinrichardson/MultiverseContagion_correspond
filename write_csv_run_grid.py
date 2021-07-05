'''run plot_grid.py after this..

and then plot_data_interactive.py or plot_data_video.py
'''

import os
import time
def run(c):
    a = os.system(c)
    return a

run("mkdir -p n_sim")


ci = 0
n_sim = 1
HzRs = [0.5 + (i/10.) for i in range(0, 10)]
sizeFs = [1. + (0.1 * i) for i in range(0, 5)]
mFs = [0.5 + (0.1 * i) for i in range(0, 10)]
total = len(HzRs) * len(sizeFs) * len(mFs)

t0 = time.time()

for HzR in HzRs:
    for sizeF in sizeFs:
        for mF in mFs:
            run("python3 write_csv_run.py 500 " + str(HzR) + " " +
                                                str(sizeF) + " " + 
                                                str(mF) + " " + 
                                                "None None " + str(n_sim))
            ci += 1

            t1 = time.time()
            secs_per_i = (t1 - t0) / ci
            eta = secs_per_i * (total - ci)

            print("% complete: " + str(100. * ci / total) + " eta: " + str(eta) + " s")
            

