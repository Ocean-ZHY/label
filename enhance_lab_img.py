import picture_enhance
from PIL import Image, ImageDraw
import numpy as np

from matplotlib.colors import rgb_to_hsv, hsv_to_rgb
#图片增强以及保存标签

def label(minr, minc, maxr, maxc, image_high, image_width):
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
    file_label:原始非yolo格式的标签
    file_image：原始图片
    file_label_name：图片增强后的标签
    file_image_name：图片增强后的图片
"""
def enhancement_label_image(file_label, file_image, file_label_name, file_image_name):
    with open(file_label) as f:
        lines = f.read()
    #a = np.random.randint(0, len(lines))
    line = lines

    file_path = file_image
    a = picture_enhance.enhancement(file_path)
    #image_data, box_data = a.normal_(file_path, line, [1920, 1080])
    #img = image_data

    #for j in range(len(box_data) - 1):
        #thickness = 3
        #left, top, right, bottom = box_data[j][0:4]
        #draw = ImageDraw.Draw(img)
        #for i in range(thickness):
            #draw.rectangle([left + i, top + i, right - i, bottom - i], outline=(255, 255, 255))
    #img.show()

    image_data, box_data = a.get_random_data(file_path, line, [1080, 1920])
    #print(box_data)
    img = Image.fromarray((image_data * 255).astype(np.uint8))
    img_high, img_width = img.size
    for j in range(len(box_data)):
        thickness = 3
        left, top, right, bottom = box_data[j][0:4]
        s = label(top, left, bottom, right, img_width, img_high)
        write_label(file_label_name, s)
        #draw = ImageDraw.Draw(img)
        #for i in range(thickness):
            #draw.rectangle([left + i, top + i, right - i, bottom - i], outline=(255, 255, 255))
    img.save(file_image_name)
    #img.show()