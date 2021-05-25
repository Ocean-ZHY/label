import os

file_path = 'F:/label_code/train/enhance_img/' #要改文件的路径
i = 1666    #标号从i的值开始，之后的每个文件依次+1
count = os.listdir(file_path)
count.sort(key=lambda x:int(x[:-4]))
for indx, j in enumerate(count):
#for j in range(len(count)):
    file_name = file_path + j
    file_new_name = file_path + str(i) + '.jpg'
    i += 1
    os.rename(file_name, file_new_name)