import zipfile
import os
class UnzipUtil(object):
    def __init__(self):

        pass

    def unzip_file(self,zipfilename, unziptodir):
        self.selfname=zipfilename
        if not os.path.exists(unziptodir):
            os.mkdir(unziptodir)

        zfobj = zipfile.ZipFile(zipfilename)
        for name in zfobj.namelist():
            name = name.replace('\\', '/')
            if name.endswith('/'):
                print(name)
                os.mkdir(os.path.join(unziptodir, name))
            else:
                ext_filename = os.path.join(unziptodir, name)
                ext_dir = os.path.dirname(ext_filename)
                print(ext_dir)
                if not os.path.exists(ext_dir):
                    os.mkdir(ext_dir)
                outfile = open(ext_filename, 'wb')
                outfile.write(zfobj.read(name))
                outfile.close()
    #unzip_file('yolo.zip', 'unziopyolo')
    def delSelf(self):
        os.remove(self.selfname)
