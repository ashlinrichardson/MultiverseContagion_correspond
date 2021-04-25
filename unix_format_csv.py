import os
import sys
args = sys.argv

if len(args) < 2:
    print("python3 unix_format_csv.py [input csv file name]"); sys.exit(1)

lines = open(args[1]).read().strip().split("\n")
lines = [x.rstrip() for x in lines]
open(args[1], "wb").write(('\r\n'.join(lines)).encode())
