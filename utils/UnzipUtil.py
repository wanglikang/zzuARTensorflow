import zipfile
import os

class UnzipUtil(object):
    def __init__(self):

        pass

    def unzip_file(self,zipfilename, unziptodir):
        self.selfname=zipfilename
        if not os.path.exists(unziptodir):
            os.mkdir(unziptodir)

        print(zipfilename)
        zfobj = zipfile.ZipFile(zipfilename)
        zfobj.extractall(path=unziptodir)
        # for names in zfobj.namelist():
        #     print(names)
        #     zfobj.extract(names, unziptodir + "_files/")
        print("解压文件成功")
    #unzip_file('yolo.zip', 'unziopyolo')
    def delSelf(self):
        os.remove(self.selfname)

'''
uu = UnzipUtil()

uu.unzip_file(r'G:\PycharmProjects\zzuARTensorflow\\utils\DIYdataV111.zip','../DIYdata')

'''