import os
import xml.etree.ElementTree as ET
import numpy as np
import cv2
import pickle
import copy
import yolo.myconfig as cfg
from os import listdir,getcwd


class data_util():
    def __init__(self,data_path):
        self.data_path = data_path
        self.cursor = 0
        self.eposh = 1
        self.labels = [filename for filename in os.listdir(os.path.join(self.data_path,"labels"))]
        self.batch_size = 25
        self.image_size = 448
        self.cell_size = 7
        self.basepath = os.path.join(getcwd(),data_path)
        print(getcwd())
        self.picpathPre = os.path.join(self.basepath,"images")

    def getTrainData(self):
        images = np.zeros((self.batch_size,self.image_size,3))
        #lables的最后一维为什么是２５？？
        lables = np.zeros((self.batch_size,self.cell_size,self.cell_size,25))
        count = 0
        while count<self.batch_size:
            imname = self.labels[count]
            print(imname)
            image = self.image_read(imname)
            label = self.load_label_from_yolo_format(imname)
            images[count] = image
            lables[count] = label

    def image_read(self, imname, flipped=False):
        imname = os.path.join(self.picpathPre,imname)[:-4]+".jpg"
        print(imname)
        image = cv2.imread(imname)
        image = cv2.resize(image, (self.image_size, self.image_size))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB).astype(np.float32)
        image = (image / 255.0) * 2.0 - 1.0
        if flipped:
            image = image[:, ::-1, :]
        return image

    def load_classes(self):
        classes = []
        f = open(os.path.join(self.data_path,"classes.txt"),'r')
        self.classes = ([cls.strip() for cls in f.readlines()])
        self.classes = dict(zip(self.classes,range(len(self.classes))))

        print(type(self.classes))
        print(self.classes)

    def load_label_from_yolo_format(self,lable_path):
        label = np.zeros((self.cell_size, self.cell_size, 25))

        lable_path = os.path.join(self.basepath,"labels", lable_path)
        print("in {}.data is:".format(lable_path))
        classid,x,y,w,h = open(lable_path,"r").readline().split()
        print("classsid:{}".format(classid))
        print("x:{}".format(x))
        print("y:{}".format(y))
        print("w:{}".format(w))
        print("w:{}".format(h))
        boxes = [x, y,w,h]
        x_ind = int(boxes[0] * self.cell_size / self.image_size)
        y_ind = int(boxes[1] * self.cell_size / self.image_size)
        label[y_ind, x_ind, 0] = 1
        label[y_ind, x_ind, 1:5] = boxes
        label[y_ind, x_ind, 5 + classid] = 1
        return label


