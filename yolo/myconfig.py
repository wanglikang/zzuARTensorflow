import os
import datetime
#
# path and dataset parameter
#
qiniuDomain = 'p7ijy2tin.bkt.clouddn.com'
'''
access_key = 'mMQxjyif6Uk8nSGIn9ZD3I19MBMEK3IUGngcX8_p'
secret_key = 'J5gFhdpQ-1O1rkCnlqYnzPiH3XTst2Szlv9GlmQM'
'''
access_key = ''
secret_key = ''

DATA_VERSION = 'V1'

DATA_ROOT_PATH = 'DIYdata'
DATA_ZIPNAME='DIYdata'+DATA_VERSION+'.zip'
DATA_DownloadZipFileName = DATA_ZIPNAME
DATA_UploadZipFileName = 'DIYdata'+DATA_VERSION+"Weights.zip"

MYDATA_PATH = os.path.join(DATA_ROOT_PATH, 'pics')
CACHE_PATH = os.path.join(DATA_ROOT_PATH, 'cache')
OUTPUT_DIR = os.path.join(DATA_ROOT_PATH, 'output')
WEIGHTS_DIR = os.path.join(DATA_ROOT_PATH, 'weights')

WEIGHTS_FILE = None
#WEIGHTS_FILE = os.path.join(DATA_ROOT_PATH, 'YOLO_small.ckpt')


CLASSES = ['aeroplane', 'bicycle', 'bird', 'boat', 'bottle', 'bus',
           'car', 'cat', 'chair', 'cow', 'diningtable', 'dog', 'horse',
           'motorbike', 'person', 'pottedplant', 'sheep', 'sofa',
           'train', 'tvmonitor','zhongtiww']

FLIPPED = True


#
# model parameter
#

IMAGE_SIZE = 448

CELL_SIZE = 7

BOXES_PER_CELL = 2

ALPHA = 0.1

DISP_CONSOLE = False

OBJECT_SCALE = 1.0
NOOBJECT_SCALE = 1.0
CLASS_SCALE = 2.0
COORD_SCALE = 5.0


#
# solver parameter
#

GPU = ''

#LEARNING_RATE = 0.0001
LEARNING_RATE = 0.001

DECAY_STEPS = 30000

DECAY_RATE = 0.1

STAIRCASE = True

BATCH_SIZE = 45

#MAX_ITER = 15000
MAX_ITER = 1500

SUMMARY_ITER = 10

#SAVE_ITER = 1000
SAVE_ITER = 100


#
# test parameter
#

THRESHOLD = 0.2

IOU_THRESHOLD = 0.5
