# simple script to show contents of a json file
import sys
import json
args = sys.argv

if len(args) < 2:
    print("python3 read_json.py params.json"); sys.exit(1)

d = json.load(open(args[1]))

for k in d:
    print('key: ' + str([k]) + ' value: ' + str([d[k]]))
