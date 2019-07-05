import re
import json
from collections import namedtuple
import requests
from .Config import config


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
    
    def __init__(self,url,videourl=None):
        self.baseVideourl = config.videourl if videourl is None else videourl
        self.url = url

    def get(self):
        response = requests.get(self.url,headers=self.headers)
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

    def form_url(self,cid):
        if cid is None:
            return None
        pm1 = str(cid)[-2:]
        pm2 = str(cid)[-4:-2]
        pm4=pm3 = str(cid)
        vurl = self.baseVideourl.format(pm1,pm2,pm3,pm4)
        return vurl



InfoTuple = namedtuple('InfoTuple','ep_id cid vurl titleFormat longTitle')

class GatherDownloader(BaseDownloader):
    def __init__(self,url, videourl=None):
        super().__init__(url,videourl)
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
        for v in vlist:
            cid = v.get('cid',None)
            titleFormat = v.get('titleFormat',None)
            longTitle = v.get('longTitle',None)
            ep_id = v.get('id',None)
            vurl = self.form_url(cid)

            yield InfoTuple(ep_id,cid,vurl,titleFormat,longTitle)


    def _save_gen_info_to_file(self):
        # import os.path
        # import urllib.parse
        # file_name = os.path.basename(urllib.parse.urlparse(self.url).path)
        # file_name = os.path.basename(urllib.parse.urlparse(self.url).path) + '_vinfo.txt'
        file_name = '_vinfo.txt'
        # print(file_name)
        with open(file_name, 'w') as f:
            for i in self.gen_info():
                f.write(json.dumps(i))
                f.write('\n')
        
        print('save to {}'.format(file_name))
        return True


class OneInGatherDownloader(GatherDownloader):
    def __init__(self,url,videourl=None):
        sp = url.split('/')
        self.ep_signature = sp[-1] if sp[-1] else sp[-2]
        
        self.isinital = False if self.ep_signature.startswith('ep') else True

        super().__init__(url,videourl)


    def create_one_info(self):
        if self.isinital:
            return next(self.gen_info())
        
        for i in self.gen_info():
            if self.ep_signature.endswith(str(i.ep_id)):
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
    def __init__(self, url, videourl=None):
        super().__init__(url,videourl)
    
    def create_one_info(self):
        content = self.get_content()

        g = re.search(r'<title.*?>(.*?)</title>', content)
        # g2 = re.search(r'"baseUrl".*?/(\d*?)-', content)
        g2 = re.search(r'"(?:base)?[U,u]rl".*?/(\d*?)-',content)

        try:
            self.name = g.groups()[0]
            self.cid = g2.groups()[0]
            self.vurl = self.form_url(self.cid)
        except AttributeError as e:
            raise e

        return InfoTuple(None,self.cid, self.vurl,self.name,self.name)


    def _save_one_info_to_file(self):
        file_name = '_single_info.txt'
        info = self.create_one_info()
        if info is None:
            print('info is Noen, failed to write to file')
            return False
        with open(file_name, 'w') as f:
            f.write(json.dumps(info))
        return True
