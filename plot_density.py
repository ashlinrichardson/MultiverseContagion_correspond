import os
import sys
import math
import numpy as np
import matplotlib.pyplot as plt
args = sys.argv

def err(m):
    print('Error: ' + m); sys.exit(1)

arguments = args[1:] # for this script the arguments are only used to create the filename

def err(m):
    print("Error:", m); sys.exit(1)

d = {}
max_N = 0
files = [x.strip() for x in os.popen("ls -1 run*.txt").readlines()]
print(len(files), "number of files")

gen_ix = 7 # index of generation field, in console.log line
max_N = 0
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
        generation = int(w[gen_ix][3:])

        print('gen', generation, 'inf', infected)
        data.append([generation, infected])

        if generation > max_N: # track the max # of generations
            max_N = generation
    d[f] = data # store the data from this run

mx = 0
value = {} # tuple indexed by file, then time
print('max_T', max_N) # max number of gen

mean = np.zeros(max_N)
for f in files:
    value[f] = np.zeros(max_N)
    data = d[f]  # time series for this file
    for i in range(len(data)):
        w = data[i] # vector for a point in time
        gen = w[0]
        value[f][gen-1] = w[1] # number of infections at point in time
        if w[1] > mx:
            mx = w[1]

    nz = 0
    for i in range(max_N): # holes need to be filled in for this datset
        if value[f][i] > 0:
            nz = value[f][i]
        elif value[f][i] == 0:
            value[f][i] = nz
        else:
            err('number of infected should be positive')

        mean[i] += value[f][i] # contribution to mean

for i in range(max_N):
    mean[i] /= len(files) # divide by N for average

f = open('mean.csv', 'wb')
f.write((str(mean[0])).encode())
for i in range(1, max_N):
    f.write(('\n' + str(mean[i])).encode())
f.close()

stdv = [np.std([value[f][i] for f in files]) for i in range(max_N)]

print("accumulate.........")
y_skip = 2. # 2 # 5.
y_inc = int(math.ceil(mx / y_skip))
x_skip = (6. / 8.) * max_N / y_inc
x_inc = int(math.ceil(max_N / x_skip))
count = np.zeros((y_inc, x_inc)) # count[k] for k in range(0,5)

print("files", files)

for f in files: # accumulate values for each file
    print(f)
    for i in range(max_N):
        v = 0
        try:
            v = value[f][i]
        except:
            pass
        idx_y = math.floor((v + (y_skip / 2.)) / y_skip)
        idx_x = math.floor((i + (x_skip / 2.)) / x_skip)
        idx_x, idx_y = max(idx_x, 0), max(idx_y, 0)
        idx_x, idx_y = min(idx_x, x_inc - 1), min(idx_y, y_inc - 1)
        count[y_inc - idx_y - 1, idx_x] += 1. # y axis is flipped

lab = "Number of Infected" # ["green","yellow","blue","red","orange"]
plt.figure(figsize=(16, 12))
plt.imshow(count)
X = np.array(range(max_N)) / x_skip
plt.plot(X, mx/y_skip -          mean/y_skip, color='red', label='mean')
plt.plot(X, mx/y_skip - (mean + stdv)/y_skip, color='green', label='mean + sigma')
plt.plot(X, mx/y_skip - (mean - stdv)/y_skip, color='blue', label='mean - sigma') 
plt.legend()
plt.xlabel('generation (rescaled)')
plt.ylabel('infected')
plt.title(lab + " (N=" + str(len(files)) + " runs) NB need to check if sims finish") # still need to adjust scales..
plt.tight_layout()
plt.savefig('_'.join(["density"] + arguments + [lab]).replace(" ", "_") + ".png")
