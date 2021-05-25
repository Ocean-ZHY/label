import cv2
import os
import glob

#path = "/home/li/data/data(RGB)/train/aug_gt_scale_0.7/3"
# 待处理图片所在地址
#paths = glob.glob(os.path.join(path, '*.jpg'))
paths = '/media/ocean/大白菜U盘/label_code/train/out/'
paths2 = '/media/ocean/大白菜U盘/label_code/train/images/'

for file in os.listdir(paths):
    file_name = paths2 + file[:-3] + 'jpg'
    img = cv2.imread(file, 0)
    if cv2.countNonZero(img) == 0:
        os.remove(file_name)