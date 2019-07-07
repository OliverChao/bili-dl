import re
import json
import requests

# 刺客五六七
url= 'https://www.bilibili.com/bangumi/play/ss6360/'
url = 'https://www.bilibili.com/bangumi/play/ep203922'

# 天行九歌
# url='https://www.bilibili.com/bangumi/play/ep118488'

# 四月谎
# url = 'https://www.bilibili.com/bangumi/play/ep80016/'
# url = 'https://www.bilibili.com/bangumi/play/ep80017/'
# url = 'https://www.bilibili.com/bangumi/play/ss1699/'
# url = 'https://www.bilibili.com/bangumi/play/ep80038'



# 画江湖
# url = 'https://www.bilibili.com/bangumi/play/ss25823/'


# # 
# url = 'https://www.bilibili.com/bangumi/play/ss26288/'

headers = {
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36'
}


response = requests.get(url,headers=headers)
# print(response.text)
content = response.text

# with open('bili.js','r') as f:
#     content = f.read()

# # pattern = 

# # g = re.search(r'"epList".*?[.*?]',content)
g = re.search(r'"epList".*?(\[.*?\])',content, re.S)

# print(g)
# print(g.groups()[0])
# print(len(g.group()))

# s = g.group()

# print(type(s))
s = g.groups()[0]
vlist = json.loads(s)
# print(vlist)


videourl = 'https://112-13-78-5.ksyungslb.com/upos-sz-mirrorks32u.acgvideo.com/upgcxcode/{}/{}/{}/{}-1-80.flv?deadline=1462165219&gen=playurl&nbs=1&oi=1879473321&os=ks3u&platform=pc&trid=80a358d94bc442babc00f32db8ced2e5&uipk=5&upsig=988ad3ae4a680b41baccaafcf80bd2a8&uparams=deadline,gen,nbs,oi,os,platform,trid,uipk&mid=165584183&ksy_gslb_referer=https%3A%2F%2Fwww.bilibili.com%2Fvideo%2Fav14063582%2F%3Fspm_id_from%3D333.788.videocard.1'

print(len(vlist))

for v in  vlist:
    print('{cid}: {titleFormat}: {longTitle}'.format(cid=v['cid'],titleFormat=v['titleFormat'],longTitle=v['longTitle']))


for v in vlist:
    pm1 = str(v['cid'])[-2:]
    pm2 = str(v['cid'])[-4:-2]
    pm4=pm3 = str(v['cid'])
    vurl = videourl.format(pm1,pm2,pm3,pm4)
    print(vurl)

    
