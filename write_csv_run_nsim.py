import os
def run(c):
    a = os.system(c)
    return a

run("mkdir -p n_sim")

for n_sim in [8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096]:
    run("rm *.txt")
    run("rm *.grep")
    run("rm *.png")
    run("rm *.csv")
    run("python3 write_csv_run.py 500 None None None None 5 " + str(n_sim))
    run("python3 plot_density.py")
    run("cp -v mean.csv n_sim/mean_" + str(n_sim) + ".csv")
    run("cp -v stdv.csv n_sim/stdv_" + str(n_sim) + ".csv")
    run("cp -v mean_sigma.png n_sim/mean_sigma_" + str(n_sim) + ".png")  

