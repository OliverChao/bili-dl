import requests
import re
import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('url',help='url')
parser.add_argument('-o','--outfile')

args = parser.parse_args()

file_name  = args.outfile

# url = 'https://www.bilibili.com/video/av30073747'
url = args.url

headers = {
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36'
    }

response = requests.get(url, headers=headers)

with open(file_name, 'w') as f:
    f.write(response.content.decode())
