# author: roczhang
# file: rice_labels.py
# time: 2021/04/22
from skimage import io
import numpy as np
import matplotlib.pyplot as plt
from skimage.color import rgb2gray
import matplotlib.patches as mpatches
from skimage import data, filters, segmentation, measure, morphology, color
import os
import enhance_lab_img as eli
import picture_enhance


#def file_txt(indx, file_name, i):
"""将标签改成yolo的标签格式
    minr:最小列
    minc:最小行
    maxr:最大列
    maxc:最大行
    image_width:图片的宽度
    image_high：图片的高度
"""
def label(minr, minc, maxr, maxc, image_width, image_high):
    width = maxc - minc
    high = maxr - minr
    x_center = (minc + maxc) / 2
    y_center = (minr + maxr) / 2
    s = '0 ' + str(x_center / image_width) + ' ' + str(y_center / image_high) + ' ' + str(width / image_width) + ' ' + str(high / image_high)
    return s


def write_label(filename, s):
    with open(filename, 'a') as f:
        f.writelines(s)
        f.writelines('\n')



"""
    file_origin_name:存放原始框最小行、最大行、最小列、最大列的数据的路径
    file_enhance_lab_name：存放图片增强后的标签的路径
    file_enhance_img_name：存放图片增强后的图片的路径
    file_name：存放原始yolo格式标签的图片路径
"""
def file_txt(indx, filename):
    #file_path = '/media/ocean/大白菜U盘/遗传算法/rice_frame/MVI_1/'
    #file_num = 1
    #file_name = file_path+str(file_num)+'.jpg'
    rice_img = io.imread(filename)
    # convert image to gray
    rice_img = rgb2gray(rice_img)
    image_high, image_width = rice_img.shape
    thresh = filters.threshold_otsu(rice_img)  # 阈值分割
    bw = morphology.closing(rice_img > thresh)  # 闭运算
    cleared = bw.copy()
    # cleared = segmentation.clear_border(cleared)  # 清除与边界相连的目标物
    label_image = measure.label(cleared)  # 连通区域的标记
    borders = np.logical_xor(bw, cleared)  # 异或
    label_image[borders] = -1

    #fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 10))
    #ax1.imshow(cleared, plt.cm.gray)
    #ax2.imshow(label_image)
    file_origin_name = '/media/ocean/大白菜U盘/label_code/train/origin_labels/' + str(indx) + '.txt'
    file_enhance_lab_name = '/media/ocean/大白菜U盘/label_code/train/enhance_lab/' + str(indx) + '.txt'
    file_enhance_img_name = '/media/ocean/大白菜U盘/label_code/train/enhance_img/' + str(indx) + '.jpg'
    file_name = '/media/ocean/大白菜U盘/label_code/train/labels/' + str(indx) + '.txt'
    for region in measure.regionprops(label_image):
        if region.area < 100:
            continue
        minr, minc, maxr, maxc = region.bbox
        num = 1
        minr, minc = minr-num, minc-num
        maxr, maxc = maxr+num, maxc+num
        #rect = mpatches.Rectangle((minc, minr), maxc - minc, maxr - minr, fill=False, edgecolor='red', linewidth=0.5)
        #ax1.add_patch(rect)
        s = '0 ' + str(minc) + ' ' + str(minr) + ' ' + str(maxc) + ' ' + str(maxr)
        write_label(file_origin_name, s)
        lab = label(minr, minc, maxr, maxc, image_width, image_high)
        write_label(file_name, lab)
    eli.enhancement_label_image(file_origin_name, filename, file_enhance_lab_name, file_enhance_img_name)
    #fig.tight_layout()
    #plt.show()


#for i in range(1,7):
#    file_path = '/media/ocean/大白菜U盘/遗传算法/rice_frame/MVI_' + str(i) + '/'
#    for indx, j in enumerate(os.listdir(file_path)):
#        file_name = file_path + j
#        file_txt(indx+1, file_name, i)
file_path = '/media/ocean/大白菜U盘/label_code/train/images/'
count = os.listdir(file_path)
count.sort(key=lambda x:int(x[:-4]))
for indx, j in enumerate(count):
    file_name = file_path + j
    file_txt(indx+1, file_name)