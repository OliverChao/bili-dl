from Bili import resources
import argparse
import requests
import re
from Bili.Config import config

parser = argparse.ArgumentParser(  
        description='crawl the bilibili in command line')   
parser.add_argument('url',help='url',default='http://')

parser.add_argument('-g','--gather',help="download the whole videos in one serial", action="store_true")
# parser.add_argument('-s','--single',help="dowbload one video")
parser.add_argument('-o','--outfile',help='generate a file for download')
parser.add_argument('-i','--readfile',help='read urls from a file')
parser.add_argument('-q','--quality',help='the quality of the video you want to download',choices=['1080+','1080','720','480','320'])

args = parser.parse_args()

url = args.url
# print(config.quality_dict)
# quality = args.quality if config.quality_dict[args.quality] else None

if args.quality is None:
    quality = None
else:
    try:
        quality = config.quality_dict[args.quality]
    except KeyError:
        quality = None
print('quaility is <{}>  **None 为默认最高品质**'.format(quality))
outfile_name = args.outfile
if args.outfile:
    r_fileSaver = resources.Aria2cFileSaver(file=outfile_name)
    isOuttoFile = True
else:
    isOuttoFile = False


url_sp = url.split('/')
ep_signature = url_sp[-1] if url_sp[-1] else url_sp[-2]

isSs = True if  ep_signature.startswith('ss') else False
isEp = True if ep_signature.startswith('ep') else False


if not isEp and not isSs and args.gather:
    print('error: av<num> can only download one by one, but you can provide a url file by using "-i".And the regular that bilibili uses is vary simple, thus you can create a url file easily.')
    exit(0)

readfile_name = args.readfile
if readfile_name:
    if isSs or isEp:
        print('ss<num> and sp<num> url is not supported url file now... you can only write av<num> in the url file')
        exit(0)
    print('read file....')
    with open(readfile_name, 'r') as f:
        for one_url in f.readlines():
            # print(one_url)
            # 需要 去掉最后读进去的 换行符
            one_url=one_url[:-1]
            r_single = resources.SingleDownloader(url=one_url,quality=quality)
            get_d = r_single.create_one_info()
            
            if not isOuttoFile:
                print(get_d)
            else:
                if len(get_d['v_split_list'])==1:
                    r_fileSaver.write(get_d['v_split_list'][0])
                    r_fileSaver.write(' out='+get_d['titleFormat']+'/'+get_d['titleFormat']+'.flv')
                else:
                    for i,one_split in enumerate(get_d['v_split_list'],start=1):
                        # if isOuttoFile:
                        r_fileSaver.write(one_split)
                        r_fileSaver.write(' out='+get_d['titleFormat']+'/'+get_d['titleFormat']+str(i)+'.flv')

    exit(0)


if not isSs and not isEp:
    r_single = resources.SingleDownloader(url=url, quality=quality)

    get_d = r_single.create_one_info()
    if not isOuttoFile:
        print(get_d)
    else:
        for i,one_split in enumerate(get_d['v_split_list'],start=1):
            # if isOuttoFile:
            r_fileSaver.write(one_split)
            r_fileSaver.write(' out='+get_d['titleFormat']+'/'+get_d['titleFormat']+str(i)+'.flv')
    exit(0)


if not args.gather:
    r_oneInGahter = resources.OneInGatherDownloader(url=url, quality=quality)
    get_d = r_oneInGahter.create_one_info()
    if not isOuttoFile:
        print(get_d)
    else:
        for i,one_split in enumerate(get_d['v_split_list'],start=1):
            # if isOuttoFile:
            r_fileSaver.write(one_split)
            r_fileSaver.write(' out='+get_d['titleFormat']+'/'+get_d['titleFormat']+str(i)+'.flv')

    exit(0)



r_gather = resources.GatherDownloader(url=url,quality=quality)

r_fileSaver = resources.Aria2cFileSaver(file=outfile_name)
for get_d in r_gather.gen_info():
    # if len(get_d['v_split_list'])==1:
    #     r_fileSaver.write(get_d['v_split_list'][0])
    #     r_fileSaver.write(' out='+get_d['titleFormat']+'/'+get_d['longTitle']+'.flv')
    # else:
    for i,one_split in enumerate(get_d['v_split_list'],start=1):
        # if isOuttoFile:
        r_fileSaver.write(one_split)
        r_fileSaver.write(' out='+get_d['titleFormat']+'/'+get_d['longTitle']+str(i)+'.flv')




def output(isOuttoFile, get_d):
    if not isOuttoFile:
        print(get_d)
    else:
        if len(get_d['v_split_list'])==1:
                    r_fileSaver.write(get_d['v_split_list'][0])
                    r_fileSaver.write(' out='+get_d['titleFormat']+'/'+get_d['titleFormat']+'.flv')
        else:
            for i,one_split in enumerate(get_d['v_split_list'],start=1):
                # if isOuttoFile:
                r_fileSaver.write(one_split)
                r_fileSaver.write(' out='+get_d['titleFormat']+'/'+get_d['titleFormat']+str(i)+'.flv')

# print(args)
# print(quality)
# print(ep_signature)
# print(isEp)

# r = resources.GatherDownloader(url=url,quality=80)

# r = resources.GatherDownloader(url=url,quality=80)
# r._save_gen_info_to_file()
# r._save_base_content_text()

# https://www.bilibili.com/bangumi/play/ss1699/
# https://www.bilibili.com/bangumi/play/ep80040/
# r = resources.OneInGatherDownloader(url=url, quality=80)
# r._save_one_info_to_file()

# r = resources.SingleDownloader(url=url, quality=80)
# a = r.create_one_info()
# print(a)

# r = resources.GatherDownloader(url=url,quality=80)
# r._save_gen_info_to_file()
# r._save_base_content_text()

# https://www.bilibili.com/bangumi/play/ss1699/
# https://www.bilibili.com/bangumi/play/ep80040/
# r = resources.OneInGatherDownloader(url=url, quality=80)
# r._save_one_info_to_file()

# r = resources.SingleDownloader(url=url, quality=80)
# a = r.create_one_info()
# print(a)

# r = resources.GatherDownloader(url=url,quality=80)
# r._save_gen_info_to_file()
# r._save_base_content_text()

# https://www.bilibili.com/bangumi/play/ss1699/
# https://www.bilibili.com/bangumi/play/ep80040/
# r = resources.OneInGatherDownloader(url=url, quality=80)
# r._save_one_info_to_file()

# r = resources.SingleDownloader(url=url, quality=80)
# a = r.create_one_info()
# print(a)
# https://www.bilibili.com/bangumi/play/ss1699/
# https://www.bilibili.com/bangumi/play/ep80040/
# r = resources.OneInGatherDownloader(url=url, quality=80)
# r._save_one_info_to_file()

# r = resources.SingleDownloader(url=url, quality=80)
# a = r.create_one_info()
# print(a)
