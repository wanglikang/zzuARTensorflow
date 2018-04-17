import os
import argparse
import datetime
import time
import tensorflow as tf
import yolo.myconfig as cfg
from utils.Uploader import Uploader

from utils.timer import Timer
from yolo.yolo_net import YOLONet
from utils.myData_util import MyDataUtil
from utils.ZipUtil import ZipUtil
import easydict

slim = tf.contrib.slim


class Solver(object):

    def __init__(self, net, data):
        self.net = net
        self.data = data
        self.weights_file = cfg.WEIGHTS_FILE
        self.max_iter = cfg.MAX_ITER
        self.initial_learning_rate = cfg.LEARNING_RATE
        self.decay_steps = cfg.DECAY_STEPS
        self.decay_rate = cfg.DECAY_RATE
        self.staircase = cfg.STAIRCASE
        self.summary_iter = cfg.SUMMARY_ITER
        self.save_iter = cfg.SAVE_ITER
        self.output_dir = os.path.join(cfg.OUTPUT_DIR, cfg.DATA_VERSION)#按照不同的数据版本存放
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        self.save_cfg()

        self.variable_to_restore = tf.global_variables()

        self.saver = tf.train.Saver(self.variable_to_restore, max_to_keep=None)
        self.ckpt_file = os.path.join(self.output_dir, 'yolo.ckpt')
        self.summary_op = tf.summary.merge_all()
        self.writer = tf.summary.FileWriter(self.output_dir, flush_secs=60)

        self.global_step = tf.train.create_global_step()
        self.learning_rate = tf.train.exponential_decay(
            self.initial_learning_rate, self.global_step, self.decay_steps,
            self.decay_rate, self.staircase, name='learning_rate')
        self.optimizer = tf.train.GradientDescentOptimizer(
            learning_rate=self.learning_rate)
        self.train_op = slim.learning.create_train_op(
            self.net.total_loss, self.optimizer, global_step=self.global_step)

        gpu_options = tf.GPUOptions()
        config = tf.ConfigProto(gpu_options=gpu_options)
        self.sess = tf.Session(config=config)
        self.sess.run(tf.global_variables_initializer())

        if self.weights_file is not None:
            print('Restoring weights from: ' + self.weights_file)
            self.saver.restore(self.sess, self.weights_file)

        self.writer.add_graph(self.sess.graph)

    def train(self):

        train_timer = Timer()
        load_timer = Timer()

        for step in range(1, self.max_iter + 1):
            print("{}:第{}轮训练".format(datetime.datetime.now().strftime('%m-%d %H:%M:%S'),step))
            time.sleep(2)
            load_timer.tic()
            images, labels = self.data.get()
            load_timer.toc()
            feed_dict = {self.net.images: images,
                         self.net.labels: labels}

            if step % self.summary_iter == 0:
                if step % (self.summary_iter * 10) == 0:

                    train_timer.tic()
                    summary_str, loss, _ = self.sess.run(
                        [self.summary_op, self.net.total_loss, self.train_op],
                        feed_dict=feed_dict)
                    train_timer.toc()
                    print('{} Epoch: {}, Step: {}, Learning rate: {}, Loss: {:5.3f}\nSpeed: {:.3f}s/iter,Load: {:.3f}s / iter, Remain: {}'.format(
                        datetime.datetime.now().strftime('%m-%d %H:%M:%S'),
                        self.data.epoch,
                        int(step),
                        round(self.learning_rate.eval(session=self.sess), 6),
                        loss,
                        train_timer.average_time,
                        load_timer.average_time,
                        train_timer.remain(step, self.max_iter)))
                else:
                    train_timer.tic()
                    summary_str, _ = self.sess.run(
                        [self.summary_op, self.train_op],
                        feed_dict=feed_dict)
                    train_timer.toc()

                self.writer.add_summary(summary_str, step)

            else:
                train_timer.tic()
                self.sess.run(self.train_op, feed_dict=feed_dict)
                train_timer.toc()

            time.sleep(1)
            if step % self.save_iter == 0:
            #if step == 1:#测试保存功能时使用此行
                print('{} Saving checkpoint file to: {}'.format(
                    datetime.datetime.now().strftime('%m-%d %H:%M:%S'),
                    self.output_dir))

                #保存图是权值
                self.saver.save(
                    self.sess, self.ckpt_file, global_step=self.global_step)
                #保存图的结构
                tf.train.write_graph(self.sess,
                                     os.path.join(cfg.OUTPUT_DIR,cfg.DATA_VERSION,'model'),
                                     'train.pbtxt')


                freezetime = datetime.datetime.now().strftime('%m-%d-%H-%M-%S')
                zu = ZipUtil()
                zu.zip_dir(os.path.join(cfg.OUTPUT_DIR,cfg.DATA_VERSION),
                           cfg.DATA_UploadZipFileName+'.'+freezetime)
                qu = Uploader()
                qu.setQiniuKEY('mMQxjyif6Uk8nSGIn9ZD3I19MBMEK3IUGngcX8_p',
                               'J5gFhdpQ-1O1rkCnlqYnzPiH3XTst2Szlv9GlmQM')
                qu.upload(cfg.DATA_UploadZipFileName+'.'+freezetime,
                          cfg.DATA_UploadZipFileName+'.'+freezetime)
                break
        print("假装已经训练完成")


    def save_cfg(self):

        with open(os.path.join(self.output_dir, 'config.txt'), 'w') as f:
            cfg_dict = cfg.__dict__
            for key in sorted(cfg_dict.keys()):
                if key[0].isupper():
                    cfg_str = '{}: {}\n'.format(key, cfg_dict[key])
                    f.write(cfg_str)



def update_config_paths(data_dir, weights_file):
    cfg.DATA_PATH = data_dir
    cfg.MYDATA_PATH = os.path.join(data_dir, 'pic')
    cfg.CACHE_PATH = os.path.join(cfg.DATA_ROOT_PATH, 'cache')
    cfg.OUTPUT_DIR = os.path.join(cfg.DATA_ROOT_PATH, 'output')
    cfg.WEIGHTS_DIR = os.path.join(cfg.DATA_ROOT_PATH, 'weights')
    cfg.WEIGHTS_FILE = os.path.join(cfg.WEIGHTS_DIR, weights_file)


def main():
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('--weights', default="YOLO_small.ckpt", type=str)
    parser.add_argument('--data_dir', default="data", type=str)
    parser.add_argument('--threshold', default=0.2, type=float)
    parser.add_argument('--iou_threshold', default=0.5, type=float)
    parser.add_argument('--gpu', default='', type=str)
    args = parser.parse_args()
    args2 = easydict.EasyDict( {
        "weights":"YOLO_small.ckpt",
        "data_dir":"data",
        "threshold":0.2,
        "gpu":"",
        "iou_threshold":0.5
    })
    print("\nargs is:{}\n".format(args))
    print(type(args))
    print(type(args.weights))
    print()
    print("\nargs2 is:{}\n".format(args2))
    print(type(args2))
    print(type(args2.weights))
    print()
    '''
    #if args.gpu is not None:
        #cfg.GPU = args.gpu
        #cfg.GPU = ''
    
    #if args.data_dir != cfg.DATA_PATH:
        #update_config_paths(args.data_dir, args.weights)
        #update_config_paths("data", "YOLO_small.ckpt")
    
    #os.environ['CUDA_VISIBLE_DEVICES'] = cfg.GPU

    datautil = MyDataUtil('DIYdata', 'train')
    yolo = YOLONet()
    solver = Solver(yolo, datautil)
    print('Start training ...')
    #solver.train()
    print("假装已经训练完毕啦")
    print('Done training.')


if __name__ == '__main__':

    # python train.py --weights YOLO_small.ckpt --gpu 0
    main()
