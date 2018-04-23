from qiniu import Auth, put_file, etag, urlsafe_base64_encode
import qiniu.config
import yolo.myconfig as cfg
import threading

class Uploader(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

        self.access_key = cfg.access_key
        self.secret_key = cfg.secret_key
        pass
    def setQiniuKEY(self,access_keym,secret_key):
        self.access_key = access_keym
        self.secret_key = secret_key

    def upload_hander(self,a,b):
        print("{} 已经上传了：{:.2f}%;{:.1f}M".format(self.filepath,a*100/b,a*1.0/1024/1024))

    def upload(self,filepath,remotefilename,mprogress_handler=None):
        self.remotefilename = remotefilename
        self.filepath = filepath
        if mprogress_handler==None:
            self.mprogress_handler = self.upload_hander

        return self
    def run(self):
        q = qiniu.Auth(self.access_key, self.secret_key)
        bucket_name = 'zzuar'
        key = self.remotefilename
        token = q.upload_token(bucket_name, key, 3600)
        localfile = self.filepath
        ret, info = put_file(token, key, localfile,progress_handler=self.mprogress_handler)
        #print(info)
        print("上传完成")
        print(self.filepath+"-->"+cfg.qiniuDomain+"/"+self.remotefilename)



'''#测试用例
qu = Uploader()
qu.setQiniuKEY('mMQxjyif6Uk8nSGIn9ZD3I19MBMEK3IUGngcX8_p','J5gFhdpQ-1O1rkCnlqYnzPiH3XTst2Szlv9GlmQM')
qu.upload('../DIYdataV1.zip','testDIYdataV1.zip',mprogress_handler=qu.upload_hander)
'''