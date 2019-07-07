import re
import time
import json
from collections import namedtuple
import requests

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


if __name__ == "__main__":
    a = FileSaver('ooo.txt')
    a.write_string('ooooooKKKKKKK')
