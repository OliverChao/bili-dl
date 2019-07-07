import re
import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument('filename')

args = parser.parse_args()

filename  = args.filename

with open(filename,'r') as f:
    content = f.read()
# print(content)


playinfo = re.search(r'window\.__playinfo__.*?(\{.*?\}.*?)</script>', content, re.S)

js  = playinfo.groups()[0]
# print(js)
d = json.loads(js)
# print(d)
print(d['data']['accept_quality'])
# print(d['data']['dash'])
# print(d['data']['durl'])

try:
    split_num = len(d['data']['durl'])
except KeyError as e:
    split_num = 1

print(split_num)