import urllib.request
import os


class DownloadUtil(object):

    def __init__(self,args):
        self.domain = 'oyqquzum6.bkt.clouddn.com/'
        self.httpDomain = 'http://oyqquzum6.bkt.clouddn.com/'
    def setDomain(self,newdomain):
        self.domain = newdomain
    # 有两种方式构造base_url的形式
    def download(self,url,path):
        #url = 'http://%s/%s' % (domain, filename)
        #localpath="./downloadfile.a"
        # 或者直接输入url的方式下载
        urllib.request.urlretrieve(url,path)
        return os.path.join(os.getcwd(),path)