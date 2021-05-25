# author: roczhang
# file: rice_labels.py
# time: 2021/04/22
from PIL import Image, ImageDraw
from skimage import io
import numpy as np
import matplotlib.pyplot as plt
from skimage.color import rgb2gray
import matplotlib.patches as mpatches
from skimage import data, filters, segmentation, measure, morphology, color
import os
import picture_enhance as pe
from picture_enhance import enhancement as eh
#def file_txt(indx, file_name, i):
def file_txt(indx, file_name):
    #file_path = '/media/ocean/大白菜U盘/遗传算法/rice_frame/MVI_1/'
    #file_num = 1
    #file_name = file_path+str(file_num)+'.jpg'
    rice_img = io.imread(file_name)
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
    #filename = '/media/ocean/大白菜U盘/遗传算法/train_labels/MVI_' + str(i) + '/' + str(indx) + '.txt'
    filename = '/media/ocean/大白菜U盘/label_code/test/labels/' + str(indx) + '.txt'
    imagename = '/media/ocean/大白菜U盘/label_code/test/image/' + str(indx) + '.jpg'

    for region in measure.regionprops(label_image):
        if region.area < 300:
            continue
        minr, minc, maxr, maxc = region.bbox
        num = 1
        minr, minc = minr-num, minc-num
        maxr, maxc = maxr+num, maxc+num
        #rect = mpatches.Rectangle((minc, minr), maxc - minc, maxr - minr, fill=False, edgecolor='red', linewidth=0.5)
        #ax1.add_patch(rect)
        width = maxc-minc
        high = maxr-minr
        x_center = (minc+maxc)/2
        y_center = (minr+maxr)/2
        #s = '0 ' + str(x_center/image_width) + ' ' + str(y_center/image_high) + ' ' + str(width/image_width) + ' ' + str(high/image_high)
        s = '0 ' + str(minc) + ' ' + str(minr) + ' ' + str(maxc) + ' ' + str(maxr)
        with open(filename, 'a') as f:
            f.writelines(s)
            f.writelines('\n')
    #fig.tight_layout()
    #plt.show()

    with open(filename) as f:
        lines = f.read()
    a = np.random.randint(0, len(lines))
    line = lines
    file_path = file_name
    image_data, box_data = eh.normal_(eh,file_path, line, [1920, 1080])
    img = image_data
    for j in range(len(box_data)):
        thickness = 3
        left, top, right, bottom = box_data[j][0:4]
        draw = ImageDraw.Draw(img)
        for i in range(thickness):
            draw.rectangle([left + i, top + i, right - i, bottom - i], outline=(255, 255, 255))
    #img.show()
    img.save(imagename)








#for i in range(1,7):
#    file_path = '/media/ocean/大白菜U盘/遗传算法/rice_frame/MVI_' + str(i) + '/'
#    for indx, j in enumerate(os.listdir(file_path)):
#        file_name = file_path + j
#        file_txt(indx+1, file_name, i)
file_path = '/media/ocean/大白菜U盘/label_code/test/images/'
#file_txt(255, file_path)
for indx, j in enumerate(os.listdir(file_path)):
    file_name = file_path + j
    file_txt(indx+1, file_name)