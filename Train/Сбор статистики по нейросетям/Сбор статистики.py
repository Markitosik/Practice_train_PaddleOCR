import os
import csv
import cv2
import datetime
from paddleocr import PaddleOCR
from jiwer import wer, cer
import re


limit = False
limitq = input('Введите количество изображений(пропустить, если все изображения): ')
ocr = PaddleOCR(rec_model_dir='C:\Studies\Practice\mark1.4', rec_image_shape="3, 32, 100"
                , rec_char_dict_path='C:/Studies/Practice1/ppocr/utils/dict1.txt')
#ocr.load_weights('inference')

file_path = 'Чистый2.csv'
images_folder_path = 'C:/Users/Mark/Downloads/dataset1/'
edited_images_folder_path = 'C:/Users/Mark/Downloads/dataset2/'

print(f'{limitq}')
if limitq != '':
    limit = True
    limitq = int(limitq)
else:
    limitq = 0


def filter_image(image_name):
    image_path = os.path.join(images_folder_path, image_name)
    img = cv2.imread(image_path)  # открываем изображение
    description_filter = 'размер 52, 200'     # описание фильтра
    height, width, _ = img.shape   # узнаем размеры изображения

    if height > 56:
        img = img[2:(-3), :]

    img = cv2.GaussianBlur(img, (3, 3), 0)
    img = cv2.resize(img, (200, 59))    # 200, 59

    # ... код фильтра

    edited_image_path = edited_images_folder_path + image_name
    cv2.imwrite(edited_image_path, img)  # сохраняем изображение
    return edited_image_path, description_filter


sum_error_wer = 0
sum_error_cer = 0
right_answer_1 = 0
current_number_file = 0
description_filter = ''
start_time = datetime.datetime.now()

if not os.path.isfile(file_path):
    print("Файла нет.")
else:
    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file)
        with open('1.csv', "w") as file:
            file.write("")

        for row in csv_reader:
            if limit is True and limitq < current_number_file + 1:
                break
            current_number_file += 1
            image_name = row[0]  # Предполагается, что имя файла находится в первом столбце (первая ячейка)

            edited_image_path, description_filter = filter_image(image_name)

            result = ocr.ocr(f'{edited_image_path}', cls=False, det=False)

            strok = str(result[0][0][0])
            strok = strok.rstrip().rstrip('\n')
            if len(strok) == 0:
                strok = "#"

            strok = re.sub(r"\s+", "", strok)    # удаляем пробелы и прочее из ответа нейронки
            row[1] = re.sub(r"\s+", "", row[1])  # удаляем пробелы и прочее из правильного ответа

            error_wer = wer(row[1], strok)
            error_cer = cer(row[1], strok)

            sum_error_wer += error_wer
            sum_error_cer += error_cer
            if strok == row[1]:
                right_answer_1 += 1
            else:
                print(image_name)
                print(strok)
                print(row[1])
                print()

    end_time = datetime.datetime.now()
    execution_time = end_time - start_time

    print('Библиотека: paddleocr en')
    print(f'Файл: {file_path}')
    print(f'Изменение изображения: чб; {description_filter}')
    print(f"Время выполнения программы: {execution_time}")
    print(f'{right_answer_1}/{current_number_file}')
    print(f'Вероятность верных ответов: {right_answer_1/(current_number_file)}')

    print(f'WER = {sum_error_wer/(current_number_file)}')
    print(f'CER = {sum_error_cer / (current_number_file)}')
    print()
