# run plot_grid.py after this..
import os
def run(c):
    a = os.system(c)
    return a

run("mkdir -p n_sim")


n_sim = 1
for HzR in [0.85 + i for i in range(0, 20)]:
    for sizeF in [1. + (0.25 * i) for i in range(0, 20)]:
        for mF in [0.75 + (0.25 * i) for i in range(0, 20)]:
            run("python3 write_csv_run.py 500 " + str(HzR) + " " +
                                                str(sizeF) + " " + 
                                                str(mF) + " " + 
                                                "None None " + str(n_sim))

