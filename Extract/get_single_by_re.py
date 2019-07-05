import re
import requests

with open('a4.txt','r')as f:
    content = f.read()


# <title data-vue-meta="true">【凌】触摸天空☁_哔哩哔哩 (゜-゜)つロ 干杯~-bilibili</title>
g = re.search(r'<title.*?>(.*?)</title>', content)

# "baseUrl":"http://upos-hz-mirrorcosu.acgvideo.com/upgcxcode/21/56/99945621/99945621-1-30015.m4s?
g2 = re.search(r'"(?:base)?[U,u]rl".*?/(\d*?)-',content)

# print(g.groups()[0])
print(g2.groups()[0])