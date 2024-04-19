import os
import csv
import shutil
import cv2
import re

file_name = 'Чистый2.csv'
train_file_name = 'train_annotation.csv'
val_file_name = 'val_annotation.csv'

images_folder_path = 'C:/Users/Mark/Downloads/dataset2/'
train_folder_path = 'C:/Studies/Practice/dataset/train/'
val_folder_path = 'C:/Studies/Practice/dataset/val/'

right_answer_1 = 0
current_number_file = 0
with open(train_folder_path+train_file_name, "w") as file:
    file.write("")

with open(val_folder_path+val_file_name, "w") as file:
    file.write("")


with open(file_name, 'r') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        if row[2] == '1':
            strok = images_folder_path+row[0]
            img = cv2.imread(strok)  # открываем изображение
            description_filter = 'размер 52, 200'  # описание фильтра
            height, width, _ = img.shape  # узнаем размеры изображения

            if height > 56:
                img = img[2:(-3), :]

            img = cv2.GaussianBlur(img, (3, 3), 0)
            img = cv2.resize(img, (200, 59))  # 200, 59

            edited_image_path = train_folder_path+"images/" + row[0]
            #print(f'"{edited_image_path}"')
            #print(cv2.imwrite(edited_image_path, img))  # сохраняем изображение
            with open(train_folder_path+train_file_name, 'a', newline='') as file1:
                writer = csv.writer(file1)
                writer.writerow([row[0], re.sub(r"\s+", "", row[1])])
        else:
            strok = images_folder_path+row[0]
            img = cv2.imread(strok)  # открываем изображение
            description_filter = 'размер 52, 200'  # описание фильтра
            height, width, _ = img.shape  # узнаем размеры изображения

            if height > 56:
                img = img[2:(-3), :]

            img = cv2.GaussianBlur(img, (3, 3), 0)
            img = cv2.resize(img, (200, 59))  # 200, 59

            edited_image_path = val_folder_path+"images/" + row[0]
            cv2.imwrite(edited_image_path, img)  # сохраняем изображение
            with open(val_folder_path+val_file_name, 'a', newline='') as file2:
                writer = csv.writer(file2)
                writer.writerow([row[0], re.sub(r"\s+", "", row[1])])
