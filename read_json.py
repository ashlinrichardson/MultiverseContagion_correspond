'''simple script to print top-level contents of a json file, by key and value e.g.:

python3 read_json.py json/case5.json 
key: ['x'] value: ['Cases,,,,,,\npID,age-Gp,comb-risk,VL,postInfD,role,minglx\n0,1,3,2.6,2.2,R,1\n1,1,3,2.6,2.2,R,1\n2,1,3,2.6,2.2,R,1\n3,1,3,2.6,2.2,R,1\n4,1,3,2.6,2.2,R,1']
'''
import sys
import json
args = sys.argv

if len(args) < 2:
    print("python3 read_json.py params.json"); sys.exit(1)

d = json.load(open(args[1]))

for k in d:
    print('key: ' + str([k]) + ' value: ' + str([d[k]]))
