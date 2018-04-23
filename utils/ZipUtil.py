import zipfile
import os
class ZipUtil(object):
    def __init__(self):
        pass

    # step　参数的意思是按照yolo.ckpt-{step}.＊的格式进行压缩，，不用全部压缩，仅仅对指定对训练轮次对结果进行压缩
    def zip_dir(self,startdir,step,file_news):
        z = zipfile.ZipFile(file_news,'w',zipfile.ZIP_DEFLATED) #参数一：文件夹名
        for dirpath, dirnames, filenames in os.walk(startdir):
            fpath = dirpath.replace(startdir,'') #这一句很重要，不replace的话，就从根目录开始复制
            fpath = fpath and fpath + os.sep or ''#这句话理解我也点郁闷，实现当前文件夹以及包含的所有文件的压缩
            for filename in filenames:
                #print(filename)
                if filename[:4]=='yolo':
                    #print("----{}".format(filename.split('.')[1].split('-')[1]))
                    if str(filename.split('.')[1].split('-')[1])==str(step):
                        z.write(os.path.join(dirpath, filename),fpath+filename)
                        print("压缩了{}".format(fpath+filename))
                else :
                    z.write(os.path.join(dirpath, filename),fpath+filename)
                    print("压缩了{}".format(fpath+filename))
            #print("for")
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