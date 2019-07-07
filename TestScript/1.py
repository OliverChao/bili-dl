import requests
import re
import json

url = 'https://api.bilibili.com/pgc/player/web/playurl?avid=29926006&cid=52137061&qn=80&type=&otype=json&ep_id=243804&fourk=1&fnver=0&fnval=16&session=890544adf400609fe15f6da39d041c13'

url = 'https://api.bilibili.com/pgc/player/web/playurl/?ep_id=86866&qn=80&bsource='

# 不加 qn 则为 默认 32
url = 'https://api.bilibili.com/pgc/player/web/playurl/?ep_id={}&qn=112&bsource='

url = url.format(80016)

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36'
}

response = requests.get(url=url,headers=headers)

# print(response.text)
js = json.loads(response.text)
print(js)
print(type(js))
print()
qualityList = js['result']['accept_quality']
print(qualityList)
print(type(qualityList))
print(112 not in qualityList)
print(len(js['result']['durl']))

