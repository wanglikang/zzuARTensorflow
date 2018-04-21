import zipfile
import os
class ZipUtil(object):

    def zip_dir(self,startdir,file_news):
        z = zipfile.ZipFile(file_news,'w',zipfile.ZIP_DEFLATED) #参数一：文件夹名
        for dirpath, dirnames, filenames in os.walk(startdir):
            print("{}".format(dirpath))
            print("{}".format(dirnames))
            print("{}".format(filenames))
            fpath = dirpath.replace(startdir,'') #这一句很重要，不replace的话，就从根目录开始复制
            fpath = fpath and fpath + os.sep or ''#这句话理解我也点郁闷，实现当前文件夹以及包含的所有文件的压缩
            #if fpath!='' and fpath.split(os.sep)[1]=='model':
            for filename in filenames:
                       #print("3filename:"+filename)
                z.write(os.path.join(dirpath, filename),fpath+filename)
            print("for")
        print ('压缩文件夹成功')
        z.close()

    def zip_files(self,files, zip_name ):
        zip = zipfile.ZipFile( zip_name, 'w', zipfile.ZIP_DEFLATED )
        for file in files:
            print ('compressing', file)
            zip.write( file )
        zip.close()
        print ('压缩文件成功 finished')

'''
    #startdir = "../DIYdatabk"  #要压缩的文件夹路径
    startdir = "G:/tempProj/Shop_ssh/src"  # 要压缩的文件夹路径
    file_news = 'G:/tempProj/Shop_ssh/DIYdataV1' +'.zip' # 压缩后文件夹的名字
    zip_dir(startdir,file_news)
'''