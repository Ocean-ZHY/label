import numpy as np
import os

#file_name = '/media/ocean/大白菜U盘/label_code/test/1/'
#file_new_name = '/media/ocean/大白菜U盘/label_code/test/2/'
file_name = '/media/ocean/大白菜U盘/YOLO/rich_train/labels/'
file_new_name = '/media/ocean/大白菜U盘/YOLO/rich_train/new_labels/'
for txt_name in os.listdir(file_name):
    txt_path = file_name + txt_name
    txt_new_path = file_new_name + str(txt_name)
    with open(txt_path,'r') as f:
        z = f.readlines()
    boxs = []
    for indx, val in enumerate(z):
        box = np.array(list(map(float, val.split())))
        s = str([box[0]]) + ' ' + str([indx+1]) + ' ' + str([box[1]]) + ' ' + str([box[2]]) + ' ' + str([box[3]]) + ' ' + str([box[4]])
        with open(txt_new_path, 'a') as fi:
            fi.writelines(s)
            fi.writelines('\n')
