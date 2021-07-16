# write csv, convert to JSON, then run simulation
import os
import sys
import multiprocessing
import uuid # uuid.uuid4()
args = sys.argv
sep = os.path.sep

def err(m):
    print("Error: " + m); sys.exit(1)

def run(c):
    print(c)
    a = os.system(c)
    if a != 0: err("command failed: " + str(c))

if len(args) < 2:
    print("python3 write_csv_run.py 500 None None None None 5 256 # example")
    err("python3 write_csv [population size] [HzR] [sizeF] [mF] [RedDays] [N_infect] [N_simulation] # write tickets going no-where for single universe")

N = None
HzR = None
sizeF = None
mF = None
RedDays = None
N_infect = None
N_simulation = None

try: N = int(args[1])
except: err("pop size needs to be a whole number")

try: HzR = float(args[2])
except: HzR = .85

try: sizeF = float(args[3])
except: sizeF = 1.5

try: mF = float(args[4])
except: mF = 0.75

try: RedDays = float(args[5])
except: RedDays = 9.4 # 11.2

try: N_infect = int(args[6])
except: N_infect = 5

try: N_simulation = int(args[7])
except: N_simulation = 128

if N_infect > N:
    err("number of initial infections must not be greater than pop size")

dn = "_".join([str(x) for x in [N, HzR, sizeF, mF, RedDays, N_infect, N_simulation]]) + sep
print(dn)
run("mkdir -p " + dn)
a = os.system("cp -rv cpp tmp run.R *.py *.js " + dn)

pfn = 'pop' + str(N) +'.csv'
f = open(dn + sep + pfn, 'wb')

def w(f, s):
    f.write(s.encode())

w(f, "Population," + str(N) + ",Universe,1,Universe\r\n")
cols = ['pID','sno','ETA', '@U', 'ETD', '>U', '@Role', '@Mx', 'Age', 'FamKey', '23-24', '00-01', '02-05', '05-06', '06-07', '07-08', '08-09', '09-10', '10-11', '11-12', '12-13', '13-14', '14-15', '15-16', '16-17', '17-18', '18-19', '19-20', '20-21', '21-22', '22-23', '23-00\r\n']

w(f, ','.join(cols))

for i in range(N):
    d = [str(i), str(0), str(0), str(0), str(24), str(0), 'R', str(1.), str(0), 'F00', '', 'U0', 'U0']

    while len(d) < len(cols):
        d = d + ['']

    w(f, ((','.join(d)) + "\r\n"))
f.close()

par_fn = 'param.csv'
f = open(dn + sep + par_fn, 'wb')
w(f, 'Parameters,,\n')
w(f, 'population,' + str(N) + ',\n')
w(f, 'UN,1,Universe\n')
w(f, 'HzR,' + str(HzR) + ',\n')
w(f, 'sizeF,' + str(sizeF) + ',0\n')
w(f, 'mF,' + str(mF) + ',0\n')
w(f, 'RedDays,' + str(RedDays) + ',\n')
w(f, 'pop file,pop' + str(N) + '.json,\n')
w(f, 'case file,case' + str(N_infect) + '.json,\n')
w(f, 'STOP,2000,\n')
f.close()

cfn = 'case' + str(N_infect) + '.csv'
f = open(dn + sep + cfn, 'wb')
w(f, '''Cases,,,,,,
pID,age-Gp,comb-risk,VL,postInfD,role,minglx''')
for i in range(N_infect):
    w(f, '\n' + str(i) + ',1,3,2.6,2.2,R,1')
f.close()

for fn in [pfn, par_fn, cfn]:
    a = os.system('cd ' + dn + '; python3 csv2json.py ' + fn)

f = open(dn + sep + 'simulation_jobs.txt', 'wb')
for i in range(N_simulation):
    f.write(('Rscript run.R > run_' + str(uuid.uuid4()) + '.txt\n').encode())
f.close()

a = os.system('cd ' + dn + '; python3 multicore.py simulation_jobs.txt ' + str(multiprocessing.cpu_count())) # let's just add one!

run("cd " + dn + "; python3 plot_density.py") # generate mean curve..
run("cd " + dn + "; python3 fit_sir.py") # fit SIR model..
# run("mv *.csv *.json *.txt *.png " + dn) # already in the directory!!
