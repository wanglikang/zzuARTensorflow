import os
import xml.etree.ElementTree as ET
import numpy as np
import cv2
import pickle
import copy
import yolo.myconfig as cfg
from utils.DownloadUtil import DownloadUtil
from utils.UnzipUtil import UnzipUtil


class MyDataUtil(object):

    def removeAllsubDir(self,path):
        for i in os.listdir(path):
            #取文件绝对路径
            path_file = os.path.join(path, i)
            if os.path.isfile(path_file):
                print("del file {}".format(path_file))
                os.remove(path_file)
            else:
                print("del dir {}".format(path_file))
                self.removeAllsubDir(path_file)
                os.removedirs(path_file)

    def prepareData(self):
        if not os.path.exists(cfg.DATA_ROOT_PATH):
            downloader = DownloadUtil()
            print("start to download data")
            filepath = downloader.download(downloader.httpDomain+'/'+cfg.DATA_ZIPNAME,cfg.DATA_ZIPNAME)
            zu = UnzipUtil()
            print("start to unzip data:{}".format(filepath))
            print("unzip to :{}".format(cfg.DATA_ROOT_PATH))
            zu.unzip_file(filepath,cfg.DATA_ROOT_PATH)
            #zu.delSelf()
            f = open(os.path.join(cfg.DATA_ROOT_PATH,'data.ok'), 'w')
            print("start to create ok file")
            f.writelines('ok')
            f.flush()
            f.close()
            print("ok for download and unzip")
        else :
            if not os.path.exists(os.path.join(cfg.DATA_ROOT_PATH,'data.ok')):
                self.removeAllsubDir(cfg.DATA_ROOT_PATH)
                self.prepareData()
                print("ok for reDownload data")


    def __init__(self,data_root_path, phase, rebuild=False):
        self.prepareData()
        print('ok for prepareData()')
        self.data_root_path = data_root_path
        self.cache_path = cfg.CACHE_PATH
        self.batch_size = cfg.BATCH_SIZE
        self.image_size = cfg.IMAGE_SIZE
        self.cell_size = cfg.CELL_SIZE
        self.classes = cfg.CLASSES
        self.class_to_ind = dict(zip(self.classes, range(len(self.classes))))
        self.classeslen = len(self.classes)
        self.flipped = cfg.FLIPPED
        self.phase = phase
        self.rebuild = rebuild
        self.cursor = 0
        self.epoch = 1
        self.gt_labels = None
        self.prepare()

    def get(self):
        images = np.zeros((self.batch_size, self.image_size, self.image_size, 3))
        labels = np.zeros((self.batch_size, self.cell_size, self.cell_size, self.classeslen+5))
        count = 0
        while count < self.batch_size:
            imname = self.gt_labels[self.cursor]['imname']
            flipped = self.gt_labels[self.cursor]['flipped']
            images[count, :, :, :] = self.image_read(imname, flipped)
            labels[count, :, :, :] = self.gt_labels[self.cursor]['label']
            count += 1
            self.cursor += 1
            if self.cursor >= len(self.gt_labels):
                np.random.shuffle(self.gt_labels)
                self.cursor = 0
                self.epoch += 1
        return images, labels

    def image_read(self, imname, flipped=False):
        image = cv2.imread(imname)
        image = cv2.resize(image, (self.image_size, self.image_size))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB).astype(np.float32)
        image = (image / 255.0) * 2.0 - 1.0
        if flipped:
            image = image[:, ::-1, :]
        return image

    def prepare(self):
        gt_labels = self.load_labels()
        #print(gt_labels[100])


        print("DIYdata1 prepare()")
        if self.flipped:
            print('Appending horizontally-flipped training examples ...')
            gt_labels_cp = copy.deepcopy(gt_labels)
            for idx in range(len(gt_labels_cp)):
                gt_labels_cp[idx]['flipped'] = True
                gt_labels_cp[idx]['label'] =\
                    gt_labels_cp[idx]['label'][:, ::-1, :]
                for i in range(self.cell_size):
                    for j in range(self.cell_size):
                        if gt_labels_cp[idx]['label'][i, j, 0] == 1:
                            gt_labels_cp[idx]['label'][i, j, 1] = \
                                self.image_size - 1 -\
                                gt_labels_cp[idx]['label'][i, j, 1]
            gt_labels += gt_labels_cp
        np.random.shuffle(gt_labels)
        self.gt_labels = gt_labels
        return gt_labels

    def load_labels(self):
        cache_file = os.path.join(
            self.cache_path, 'mydata_' + self.phase + '_gt_labels.pkl')

        if os.path.isfile(cache_file) and not self.rebuild:
            print('Loading gt_labels from: ' + cache_file)
            with open(cache_file, 'rb') as f:
                gt_labels = pickle.load(f)
            return gt_labels

        print('Processing gt_labels from: ' + self.data_root_path)

        if not os.path.exists(self.cache_path):
            os.makedirs(self.cache_path)

        if self.phase == 'train':
            txtname = os.path.join(
                self.data_root_path,'cfg','trainval.txt')
        else:
            txtname = os.path.join(
                self.data_root_path, 'test.txt')

        with open(txtname, 'r') as f:
            self.image_index = [x.strip() for x in f.readlines()]

        gt_labels = []
        for index in self.image_index:
            print("image_index is:{}".format(index))
            label, num = self.load_pascal_annotation(index)
            if num == 0:
                continue
            imname = os.path.join(self.data_root_path,'pics', index + '.jpg')
            gt_labels.append({'imname': imname,
                              'label': label,
                              'flipped': False})
        print('Saving gt_labels to: ' + cache_file)
        with open(cache_file, 'wb') as f:
            pickle.dump(gt_labels, f)
        return gt_labels

    def load_pascal_annotation(self, index):
        """
        Load image and bounding boxes info from XML file in the PASCAL VOC
        format.
        """

        imname = os.path.join(self.data_root_path, 'pics',index + '.jpg')
        im = cv2.imread(imname)
        h_ratio = 1.0 * self.image_size / im.shape[0]
        w_ratio = 1.0 * self.image_size / im.shape[1]
        # im = cv2.resize(im, [self.image_size, self.image_size])

        label = np.zeros((self.cell_size, self.cell_size, self.classeslen+5))
        
        filename = os.path.join(self.data_root_path, 'pics',index + '.xml')
        tree = ET.parse(filename)
        objs = tree.findall('object')

        for obj in objs:
            bbox = obj.find('bndbox')
            # Make pixel indexes 0-based
            x1 = max(min((float(bbox.find('xmin').text) - 1) * w_ratio, self.image_size - 1), 0)
            y1 = max(min((float(bbox.find('ymin').text) - 1) * h_ratio, self.image_size - 1), 0)
            x2 = max(min((float(bbox.find('xmax').text) - 1) * w_ratio, self.image_size - 1), 0)
            y2 = max(min((float(bbox.find('ymax').text) - 1) * h_ratio, self.image_size - 1), 0)
            print(imname)
            print(obj.find('name').text.lower().strip())
            cls_ind = self.class_to_ind[obj.find('name').text.lower().strip()]


            boxes = [(x2 + x1) / 2.0, (y2 + y1) / 2.0, x2 - x1, y2 - y1]
            x_ind = int(boxes[0] * self.cell_size / self.image_size)
            y_ind = int(boxes[1] * self.cell_size / self.image_size)
            if label[y_ind, x_ind, 0] == 1:
                continue
            label[y_ind, x_ind, 0] = 1
            label[y_ind, x_ind, 1:5] = boxes
            label[y_ind, x_ind, 5 + cls_ind] = 1

        return label, len(objs)
