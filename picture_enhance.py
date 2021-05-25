from PIL import Image, ImageDraw
import numpy as np
from matplotlib.colors import rgb_to_hsv, hsv_to_rgb

"""
    进行图片增强与标签的转换
"""

class enhancement(object):
    def __init__(self, file_path):
        self.file_path = file_path

    def rand(self, a=0, b=1):
        return np.random.rand() * (b - a) + a

    def get_random_data(self, file_path, annotation_line, input_shape, random=True, max_boxes=20, jitter=.5, hue=.1, sat=1.5, val=1.5,
                        proc_img=True):
        '''random preprocessing for real-time data augmentation'''
        line = annotation_line.split('\n')
        line.pop()
        line = np.array(line)
        # image = Image.open(line[0])
        image = Image.open(file_path)
        iw, ih = image.size
        h, w = input_shape
        # box = np.array([np.array(list(map(int, box.split(',')))) for box in line[1:]])

        box = []
        for boxs in line:
            boxs = np.array(list(map(float, boxs.split())))
            box.append(boxs[1:])
        box = np.array(box)
        # 对图像进行缩放并且进行长和宽的扭曲
        new_ar = w / h * self.rand(1 - jitter, 1 + jitter) / self.rand(1 - jitter, 1 + jitter)
        scale = self.rand(.25, 2)
        if new_ar < 1:
            nh = int(scale * h)
            nw = int(nh * new_ar)
        else:
            nw = int(scale * w)
            nh = int(nw / new_ar)
        image = image.resize((nw, nh), Image.BICUBIC)

        # 将图像多余的部分加上灰条
        dx = int(self.rand(0, w - nw))
        dy = int(self.rand(0, h - nh))
        new_image = Image.new('RGB', (w, h), (128, 128, 128))
        new_image.paste(image, (dx, dy))
        image = new_image

        # 翻转图像
        flip = self.rand() < .5
        if flip: image = image.transpose(Image.FLIP_LEFT_RIGHT)

        # 色域扭曲
        hue = self.rand(-hue, hue)
        sat = self.rand(1, sat) if self.rand() < .5 else 1 / self.rand(1, sat)
        val = self.rand(1, val) if self.rand() < .5 else 1 / self.rand(1, val)
        x = rgb_to_hsv(np.array(image) / 255.)
        x[..., 0] += hue
        x[..., 0][x[..., 0] > 1] -= 1
        x[..., 0][x[..., 0] < 0] += 1
        x[..., 1] *= sat
        x[..., 2] *= val
        x[x > 1] = 1
        x[x < 0] = 0
        image_data = hsv_to_rgb(x)  # numpy array, 0 to 1

        # 将box进行调整
        box_data1 = []
        if len(box) > 0:
            np.random.shuffle(box)
            box[:, [0, 2]] = box[:, [0, 2]] * nw / iw + dx
            box[:, [1, 3]] = box[:, [1, 3]] * nh / ih + dy
            if flip: box[:, [0, 2]] = w - box[:, [2, 0]]
            box[:, 0:2][box[:, 0:2] < 0] = 0
            box[:, 2][box[:, 2] > w] = w
            box[:, 3][box[:, 3] > h] = h
            box_w = box[:, 2] - box[:, 0]
            box_h = box[:, 3] - box[:, 1]
            box = box[np.logical_and(box_w > 1, box_h > 1)]  # discard invalid box
            #if len(box) > max_boxes: box = box[:max_boxes]
            box_data = np.zeros((len(box), 4))
            box_data[:len(box)] = box

        return image_data, box_data

    def normal_(self, file_path, annotation_line, input_shape):
        '''random preprocessing for real-time data augmentation'''
        line = annotation_line.split('\n')
        image = Image.open(file_path)
        line.pop()
        line = np.array(line)
        # box = np.array([np.array(list(map(int, box.split(',')))) for box in line[:, 1:]])
        boxs = []
        for box in line:
            box = np.array(list(map(int, box.split())))
            boxs.append(box[1:])
        boxs = np.array(boxs)
        return image, boxs