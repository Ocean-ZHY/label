import json
import re
import os
import glob
import cv2

def mathxyxy(x, y, w, h, image_w, image_h):
    #new_x = x * 2 * image_w #minc + maxc
    #new_y = y * 2 * image_h #minr + maxr
    #new_w = w * image_w
    #new_h = h * image_h
    #maxc = (new_x + new_w)/2
    #maxr = (new_y + new_h)/2
    #minr = maxr - new_h
    #minc = maxc - new_w
    new_x = x * image_w
    new_y = y * image_h
    new_w = w * image_w
    new_h = h * image_h
    minc = new_x - new_w/2
    maxc = new_x + new_w/2
    minr = new_y - new_h/2
    maxr = new_y + new_h/2


    return minr, minc, maxr, maxc
# txt文件路径
#txt_dir_name = "D:/python/yolov5-master/inference/111"
txt_dir_name = "/media/ocean/大白菜U盘/label_code/train/enhance_lab"
json_pattern = os.path.join(txt_dir_name, '*.txt')
file_list = glob.glob(json_pattern)
for file in file_list:
    # 找到图片名
    name1 = os.path.basename(file)
    name = os.path.splitext(name1)[0]
    pic_name = name + '.jpg'
    pic_path = "/media/ocean/大白菜U盘/label_code/train/enhance_img/" + pic_name
    img = cv2.imread(pic_path)
    h, w, c = img.shape
    # 读取文件
    with open(file, 'r', encoding="utf-8") as txt_file:
        # 建立shape用以存储shapes里面的数据
        shape = []
        # 逐行读取
        for line in txt_file:
            # 每一行是一个字典
            # 将第一行数据按空格切分
            line = line.strip().split()
            label_n = line[0]
            points1 = []
            minr, minc, maxr, maxc = mathxyxy(float(line[1]), float(line[2]), float(line[3]), float(line[4]), w, h)
            points1.append([minc, minr])
            points1.append([maxc, maxr])
            #points1.append([float(line[1]), float(line[2])])
            #points1.append([float(line[3]), float(line[4])])
            shape.append({"label": label_n, "points": points1, "group_id": None, "shape_type": "rectangle", "flags": {}})
    # 创建一个字典
    result = {"version": "4.5.6", "flags": {}, "shapes": shape, "imagePath": pic_name, "imageData": None, "imageHeight": h, "imageWidth": w, "lineColor": [0, 255, 0, 128], "fillColor": [255, 0, 0, 128]}
    # 设置json存储路径
    json_path = "/media/ocean/大白菜U盘/label_code/train/json_file/" + name + ".json"
    # 将字典转换为字符串
    # json_str = json.dumps(result, indent=4)
    # 将字典写入json文件中
    with open(json_path, 'w') as json_file:
        json.dump(result, json_file, indent=4)
        #json_file.write(json_str)