import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('file',help="file")
args = parser.parse_args()

f_name = args.file

with open(f_name,'r') as f:
    for i in f.readlines():
        d = json.loads(i)
        print(d['titleFormat'],d['longTitle'])

