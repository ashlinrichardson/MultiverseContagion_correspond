import os
import sys

files = os.popen('find ./ -name beta_gamma_R0.csv').readlines()
files = [x.strip() for x in files]
for f in files:
    cmd = 'rm ' + f
    print(cmd)
    a = os.system(cmd)



