import xml.etree.ElementTree as ET
from os import getcwd

classes = ["bot", "red_armor", "blue_armor"]

def convert_annotation(image_id, list_file):
    in_file = open("%s.xml"%image_id)
    tree = ET.parse(in_file)
    root = tree.getroot()

    for obj in root.iter('object'):
        class_id = 0
        if obj.find('name').text == "ignore":
            continue
        if obj.find('name').text == "armor":
            if obj.find("armor_color").text == "red": class_id = 1
            if obj.find("armor_color").text == "blue": class_id = 2
        else:
            difficult = obj.find('difficulty').text
            if int(difficult) == 2: continue
        xmlbox = obj.find('bndbox')
        b = (round(float(xmlbox.find('xmin').text)), 
             round(float(xmlbox.find('ymin').text)), 
             round(float(xmlbox.find('xmax').text)), 
             round(float(xmlbox.find('ymax').text)))
        list_file.write(" " + ",".join([str(a) for a in b]) + ',' + str(class_id))

image_ids = open(r'F:\RM\DJI_ROCO\train.txt').read().strip().split()
list_file = open(r'F:\RM\yolo3-keras\train.txt', 'w')
for image_id in image_ids:
    print(image_id)
    temp = image_id.replace("image_annotation", "image")
    list_file.write("%s.jpg"%temp)
    convert_annotation(image_id, list_file)
    list_file.write('\n')
list_file.close()
