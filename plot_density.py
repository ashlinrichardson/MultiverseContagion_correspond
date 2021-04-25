import os
import sys
import math
import numpy as np
import matplotlib.pyplot as plt
args = sys.argv

def err(m): print('Error: ' + m); sys.exit(1)

arguments = args[1:] # for this script the arguments are only used to create the filename

def err(m):
    print("Error:", m); sys.exit(1)

d = {}
max_N = 0
files = [x.strip() for x in os.popen("ls -1 run*.txt").readlines()]
print(len(files), "number of files")


gen_ix = 7 # index of generation field, in console.log line
for f in files:
    g = f[:-4] + '.grep'
    a = os.system('grep "prob=" ' + f + ' > ' + g)
    lines = [x.strip() for x in open(g).readlines()]
    print(lines)

    data = []
    for i in range(len(lines)):
        generation = 0
        infected = 0 # set these from the console.log line
        w = lines[i].strip().split()
        if w[0][-1] != 'I': err('console.log line: expected I')
        infected = int(w[0][:-1])
        if w[gen_ix][0:3] != 'gen': # recover from variable gen field loc
            for j in range(len(w)):
                if w[j][0:3] == 'gen':
                    gen_ix = j
                    break
        generation = w[gen_ix][3:]

        print('gen', generation, 'inf', infected)

    sys.exit(1)
    exp = '"","green","yellow","blue","red","orange"'
    if lines[0] != exp: err("expected: " + exp)

    data = []    
    for i in range(len(lines)):
        w = lines[i].strip().split(',')
        w = [x.strip('"') for x in w]
        if i > 0:
            w = [int(x) for x in w] # read non-header row
            data.append(w)

    N = len(data)
    if N > max_N: max_N = N  # max number of iter observed in batch 
    d[f] = data

value = {} # heterogeneous tuple indexed by file, colour, then time

print(value)
print('max_T', max_N)
max_T = max_N

ci = 1
mn, mx = 0, 0 # observed min and max, assume min = 0
for f in files:
    value[f] = [np.zeros(max_N) for i in range(5)] # average value 
    print(ci, f)
    ci += 1
    data = d[f]  # time series for this file
    for i in range(len(data)):
        w = data[i] # vector for a point in time
        j = w[0] - 1
        w = w[1:]
        if len(w) != 5:
            print("Error: vector length expected: 5")
        for k in range(5): # for each dimension of vector
            value[f][k][j] = w[k]
            if mx < w[k]:
                mx = w[k]
            

#print("value", value)
#print(mx)
print("accumulate.........")
y_skip = 2 # 5.
y_inc = int(math.ceil(mx / y_skip))
x_skip = (6. / 8.) * max_N / y_inc
x_inc = int(math.ceil(max_N / x_skip))
count = [np.zeros((y_inc, x_inc)) for i in range(5)] # one grid for each color

print("files", files)

for f in files: # accumulate values for each file
    print(f)
    for k in range(5):
        for i in range(max_T):
            v = 0
            try: v = value[f][k][i]
            except: pass
            # print("v,i", v, i)
            idx_y = math.floor((v + (y_skip / 2.)) / y_skip)
            idx_x = math.floor((i + (x_skip / 2.)) / x_skip)
            idx_x, idx_y = max(idx_x, 0), max(idx_y, 0)
            idx_x, idx_y = min(idx_x, x_inc - 1), min(idx_y, y_inc - 1)
            # print("idx", idx_x, "idy", idx_y, "xinc", x_inc, "yinc", y_inc)
            count[k][y_inc - idx_y - 1, idx_x] += 1. # y axis is flipped

lab = ["green","yellow","blue","red","orange"]
for k in range(len(lab)):
    plt.figure(figsize=(16, 12))
    # plt.rcParams['axes.facecolor'] = 'black'
    plt.imshow(count[k])
    print(count[k].shape)
    print(count[k])
    plt.title(lab[k] + " N=" + str(len(files))) # + " (still need to adjust scales..)")
    plt.tight_layout()
    plt.savefig('_'.join(["density"] + arguments + [lab[k]]) + ".png")
