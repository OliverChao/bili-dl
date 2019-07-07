import re
import time
import json
from collections import namedtuple
import requests
from .Config import config
from concurrent import futures


class FileSaver(object):
    def __init__(self, file):
        self.file_name = file
        self._f = open(file, 'w', encoding='utf_8')

    def __del__(self):
        """关闭文件，并将文件号和文件名都清空"""
        self._f.close()
        del self._f
        del self.file_name
        # print('close file successfully....')

    def write_string(self, string):
        """向对象中打开的文件写入字符串，会自动加入换行"""
        self._f.write(string + '\n')


class Aria2cFileSaver(FileSaver):
    def __init__(self, file=None):
        filename = 'aria2c.down'  if file is None else file
        super().__init__( file=filename )
    
    def write(self, url, out=None):
        self.write_string( url )
        if out is not None:
            self.write_string( out )
        pass


class BaseDownloader(object):
    
    headers = config.headers
    
    def __init__(self,url,quality=None):
        self.quality = quality
        self.baseVideourl = config.videourl
        self.url = url

    def get(self):
        response = requests.get(self.url, headers=self.headers)
        # return response.text
        return response
    
    def get_content(self):
        return self.get().text

    def _save_base_content_text(self):
        # import os.path
        # import urllib.parse
        # file_name = os.path.basename(urllib.parse.urlparse(self.url)) + '.txt'
        file_name = 'base_content.txt'
        response = self.get()
        with open(file_name,'w') as f:
            f.write(response.text)
        print('save to {}'.format(file_name))
        return True

    def form_url(self,cid,num,quality):
        if cid is None:
            return None
        pm1 = str(cid)[-2:]
        pm2 = str(cid)[-4:-2]
        pm4=pm3 = str(cid)
        vurl = self.baseVideourl.format(pm1=pm1, pm2=pm2, cid=pm3, cid2=pm4 ,num=num, quality=quality)
        return vurl


InfoTuple = namedtuple('InfoTuple','ep_id cid vurl titleFormat longTitle')

class GatherDownloader(BaseDownloader):
    def __init__(self,url, quality=None):
        super().__init__(url, quality)
        pass
    
    def _vurl_info(self):
        content = self.get_content()
        g = re.search(r'"epList".*?(\[.*?\])',content, re.S)
        s = g.groups()[0]
        vlist = json.loads(s)
        return vlist
        
    def gen_info(self):
        # print('{cid}: {titleFormat}: {longTitle}'.format(cid=v['cid'],titleFormat=v['titleFormat'],longTitle=v['longTitle']))
        vlist = self._vurl_info()

        with futures.ThreadPoolExecutor(max_workers=20) as exectutor:
            g = exectutor.map(self._generate_one_info, vlist)

        return g
        
        # for v in vlist:
        #     d={}
        #     d['cid'] = v.get('cid',None)
        #     d['titleFormat'] = v.get('titleFormat',None)
        #     d['longTitle'] = v.get('longTitle',None)
        #     d['ep_id'] = v.get('id',None)
        #     self.analyze_ep_id(d['ep_id'])
        #     d['v_split_list'] = []

        #     for i in range(self.split_num):
        #         vurl = self.form_url(d['cid'], i+1, self.quality)
        #         d['v_split_list'].append(vurl)

        #     # yield InfoTuple(ep_id,cid,v_split_list,titleFormat,longTitle)
        #     yield d

    def _generate_one_info(self,v):
        d={}
        d['cid'] = v.get('cid',None)
        d['titleFormat'] = v.get('titleFormat',None)
        d['longTitle'] = v.get('longTitle',None)
        d['ep_id'] = v.get('id',None)
        num = self.analyze_ep_id(d['ep_id'])
        d['v_split_list'] = []

        for i in range(num):
            vurl = self.form_url(d['cid'], i+1, self.quality)
            d['v_split_list'].append(vurl)
        return d


    def analyze_ep_id(self, ep_id):
        # url qn 为品质, 抓出来的 数据 >= qn
        url = 'https://api.bilibili.com/pgc/player/web/playurl/?ep_id={}&qn=112&bsource='
        url = url.format(ep_id)
        # print('start {} at {}'.format(ep_id, time.ctime()))
        response = requests.get(url=url,headers=self.headers)
        js = json.loads(response.text)
        try:
            qualityList = js['result']['accept_quality']
        except KeyError: 
            # 可能: {"code":-10403,"message":"大会员专享限制"}
            print(response.text)
            return 0
        if self.quality is None or self.quality not in qualityList:
            self.quality = qualityList[0]

        split_num = len(js['result']['durl'])
        return split_num

    def _save_gen_info_to_file(self):
        # import os.path
        # import urllib.parse
        # file_name = os.path.basename(urllib.parse.urlparse(self.url).path)
        # file_name = os.path.basename(urllib.parse.urlparse(self.url).path) + '_vinfo.txt'
        file_name = '_vinfo.json'
        # print(file_name)
        with open(file_name, 'w') as f:
            for i in self.gen_info():
                f.write(json.dumps(i))
                f.write('\n')
        
        print('save to {}'.format(file_name))
        return True


class OneInGatherDownloader(GatherDownloader):
    def __init__(self,url,quality=None):
        sp = url.split('/')
        self.ep_signature = sp[-1] if sp[-1] else sp[-2]
        
        # 如果给 ss<num> 这样的url, 则直接给番剧的第一个数据, 如果是ep<num> 这样的url, 则下载 ep<num>
        self.isinital = False if self.ep_signature.startswith('ep') else True

        super().__init__(url, quality)

    def create_one_info(self):
        if self.isinital:
            return next(self.gen_info())
        
        for i in self.gen_info():
            if self.ep_signature.endswith(str(i['ep_id'])):
                return i
        return None

    def _save_one_info_to_file(self):
        file_name = '_one_info.txt'
        info = self.create_one_info()
        if info is None:
            print('info is Noen, failed to write to file')
            return False
        with open(file_name, 'w') as f:
            f.write(json.dumps(info))
        return True


class SingleDownloader(BaseDownloader):
    def __init__(self, url, quality=None):
        super().__init__(url, quality)

    def create_one_info(self):
        content = self.get_content()    
        d = {}
        playinfo = re.search(r'window\.__playinfo__.*?(\{.*?\}.*?)</script>', content, re.S)
        
        try:
            js  = playinfo.groups()[0]
        except AttributeError as e:
            print('extract play info error')
            raise e
        
        # print(js)
        try:
            data = json.loads(js)    
        except json.decoder.JSONDecodeError as e:
            print('json parse error when parse playinfo')
            raise e
        
        qualityList = data['data']['accept_quality']
        if self.quality is None or self.quality not in qualityList:
            self.quality = qualityList[0]

        try:
            split_num = len(data['data']['durl'])
        except KeyError as e:
            split_num = 1
        
        


        g = re.search(r'<title.*?>(.*?)</title>', content)
        # g2 = re.search(r'"baseUrl".*?/(\d*?)-', content)
        g2 = re.search(r'"(?:base)?[U,u]rl".*?/(\d*?)-',content)
        try:
            self.name = g.groups()[0]
            self.cid = g2.groups()[0]
            # self.vurl = self.form_url(self.cid)
        except AttributeError as e:
            print('get name or cid error')
            raise e
        else:
            d['cid'] =self.cid
            d['titleFormat'] = d['longTitle'] = self.name
            d['ep_id'] = None
            pass

        d['v_split_list'] = []
        for i in range(split_num):
            d['v_split_list'].append( self.form_url(self.cid, i+1, self.quality) )

        return d
        # return InfoTuple(None,self.cid, self.vurl,self.name,self.name)

    def _save_one_info_to_file(self):
        file_name = '_single_info.txt'
        info = self.create_one_info()
        if info is None:
            print('info is Noen, failed to write to file')
            return False
        with open(file_name, 'w') as f:
            f.write(json.dumps(info))
        return True

