from Bili import resources
import argparse
import requests
import re


parser = argparse.ArgumentParser(  
        description='crawl the bilibili in command line')   
parser.add_argument('url',help='url')
# parser.add_argument('-w','--windowns', help='if add this op, change the file to windows type',action='store_true')

# parser.add_argument('-g','--gather',help="download the whole videos in one serial")
# parser.add_argument('-s','--single',help="dowbload one video")

args = parser.parse_args()

url = args.url

r = resources.GatherDownloader(url=url)
r._save_gen_info_to_file()
r._save_base_content_text()

# r = resources.SingleDownloader(url=url)
# a = r.create_one_info()
# print(a)
