from utils.testdata_util import data_util
import os
import datetime

if __name__ == '__main__':
   # testutil = data_util("../DIYdata")
#    testutil.load_classes()
#    testutil.getTrainData()
    epoch = 1
    step =2
    loss =5
    sttr="dede"
    log_str = '{} Epoch: {}, Step: {}, Lear rate: {}, Loss: {:5.3f}\nSpeed: {:.3f}s/iter,Load: {:.3f}s / iter, Remain: {}'.format(
        datetime.datetime.now().strftime('%m-%d %H:%M:%S'),
        epoch,
        int(step),
        23,
        loss,
        3,
        4,
        sttr)
    print(log_str)

'''
    pic_path = "/home/wlk/Develop/gitDownload/yolo_tensorflow/DIYdata/pics"
    filenames = []
    filenames = [x[:-4] for x in os.listdir(pic_path) if x[-4:] == ".jpg"]
    for nam in filenames:
       print(nam)
    print(len(filenames))
'''