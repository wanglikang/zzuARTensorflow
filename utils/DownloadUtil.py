import urllib.request
import os
import yolo.myconfig as cfg


class DownloadUtil(object):

    def __init__(self):
        #self.domain = 'oyqquzum6.bkt.clouddn.com/'
        self.domain = cfg.qiniuDomain+'/'
        #self.httpDomain = 'http://oyqquzum6.bkt.clouddn.com/'
        self.httpDomain = 'http://'+self.domain
        #http://p7ijy2tin.bkt.clouddn.com/DIYdataV1.zip
    def setDomain(self,newdomain):
        self.domain = newdomain
    # 有两种方式构造base_url的形式
    def download(self,url,path):
        #url = 'http://%s/%s' % (domain, filename)
        #localpath="./downloadfile.a"
        # 或者直接输入url的方式下载
        if not os.path.exists(path):
            urllib.request.urlretrieve(url,path)
            print('{} download done'.format(url))
        return os.path.join(os.getcwd(),path)