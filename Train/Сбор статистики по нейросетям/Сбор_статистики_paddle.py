import os
import csv
import cv2
import datetime
from paddleocr import PaddleOCR
from jiwer import wer, cer
import re

limit = False
limitq = input('Введите количество изображений: ')
ocr = PaddleOCR(lang='en')

print(f'"{limitq}"')
if limitq != '':
    limit = True
    limitq = int(limitq)
else:
    limitq = 0

file_path = 'Чистый2.csv'
images_folder_path = 'C:/Users/Mark/Downloads/dataset1/'

for i in range(0, 1):
    print(i)
    filter = ''
    sum_error_wer = 0
    sum_error_cer = 0
    right_answer_1 = 0
    current_number_file = 0
    start_time = datetime.datetime.now()
    if not os.path.isfile(file_path):
        print("Файла нет.")
    else:
        with open(file_path, 'r') as file:
            csv_reader = csv.reader(file)
            with open('1.csv', "w") as file:
                file.write("")
            if i == 1:
                filter = 'resize: 104*416'
            elif i == 2:
                    filter = 'resize: 104*416; height > 50 -> обрез по 2 сверху и снизу'
            elif i == 3:
                filter = 'resize: 50*200'
            elif i == 4:
                    filter = 'resize: 50*200; height > 50 -> обрез по 2 сверху и снизу'
            elif i == 5:
                filter = 'resize: 52*200'
            elif i == 6:
                    filter = 'resize: 52*200; height > 50 -> обрез по 2 сверху и снизу'
            elif i == 7:
                    filter = 'resize: 52*200; height > 48 -> обрез по 2 сверху и снизу'
            elif i == 8:
                    filter = 'resize: 52*200; height > 52 -> обрез по 2 сверху и снизу'
            elif i == 9:
                filter = 'resize: 52*208'
            elif i == 10:
                    filter = 'resize: 52*208; height > 50 -> обрез по 2 сверху и снизу'
            elif i == 11:
                    filter = 'resize: 52*208; height > 48 -> обрез по 2 сверху и снизу'
            elif i == 12:
                    filter = 'resize: 52*208; height > 52 -> обрез по 2 сверху и снизу'
            elif i == 13:
                filter = 'resize: *1.5 *1.5'
            elif i == 14:
                    filter = 'resize: *1.5 *1.5; height > 50 -> обрез по 2 сверху и снизу'

            for row in csv_reader:
                if limit is True and limitq < current_number_file:
                    break
                current_number_file += 1
                image_name = row[0]  # Предполагается, что имя файла находится в первом столбце (первая ячейка)
                image_path = os.path.join(images_folder_path, image_name)

                img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
                height, width = img.shape
                if i == 1:
                    img = cv2.resize(img, (416, 104))
                    img = cv2.GaussianBlur(img, (5, 5), 5)
                    #filter = 'resize: 104*416'
                elif i == 2:
                    img = cv2.resize(img, (416, 104))
                    if height > 50:
                        img = img[2:(-2), :]

                        #filter = 'resize: 104*416; height > 50 -> обрез по 2 сверху и снизу'
                elif i == 3:
                    img = cv2.resize(img, (200, 50))
                    #filter = 'resize: 50*200'
                elif i == 4:
                    img = cv2.resize(img, (200, 50))
                    if height > 50:
                        img = img[2:(-2), :]
                        #filter = 'resize: 50*200; height > 50 -> обрез по 2 сверху и снизу'
                elif i == 5:
                    img = cv2.resize(img, (200, 52))
                    #filter = 'resize: 52*200'
                elif i == 6:
                    img = cv2.resize(img, (200, 52))
                    if height > 50:
                        img = img[2:(-2), :]
                        #filter = 'resize: 52*200; height > 50 -> обрез по 2 сверху и снизу'
                elif i == 7:
                    img = cv2.resize(img, (200, 52))
                    if height > 48:
                        img = img[2:(-2), :]
                        #filter = 'resize: 52*200; height > 48 -> обрез по 2 сверху и снизу'
                elif i == 8:
                    img = cv2.resize(img, (200, 52))
                    if height > 52:
                        img = img[2:(-2), :]
                        #img = cv2.GaussianBlur(img, (5, 5), 5)
                        #filter = 'resize: 52*200; height > 52 -> обрез по 2 сверху и снизу'
                elif i == 9:
                    img = cv2.resize(img, (208, 52))
                    #filter = 'resize: 52*208'
                elif i == 10:
                    img = cv2.resize(img, (208, 52))
                    if height > 50:
                        img = img[2:(-2), :]
                        #filter = 'resize: 52*208; height > 50 -> обрез по 2 сверху и снизу'
                elif i == 11:
                    img = cv2.resize(img, (208, 52))
                    if height > 48:
                        img = img[2:(-2), :]
                        #filter = 'resize: 52*208; height > 48 -> обрез по 2 сверху и снизу'
                elif i == 12:
                    img = cv2.resize(img, (208, 52))
                    if height > 52:
                        img = img[2:(-2), :]
                        #filter = 'resize: 52*208; height > 52 -> обрез по 2 сверху и снизу'
                elif i == 13:
                    img = cv2.resize(img, None, fx=1.5, fy=1.5)
                    #filter = 'resize: *1.5 *1.5'
                elif i == 14:
                    img = cv2.resize(img, None, fx=1.5, fy=1.5)
                    if height > 50:
                        img = img[2:(-2), :]
                        #filter = 'resize: *1.5 *1.5; height > 50 -> обрез по 2 сверху и снизу'

                cv2.imwrite(f'C:/Users/Mark/Downloads/dataset2/{image_name}', img)

                result = ocr.ocr(f'C:/Users/Mark/Downloads/dataset2/{image_name}', cls=False, det=False)
                strok = str(result[0][0][0])
                strok = strok.rstrip().rstrip('\n')
                if len(strok) == 0:
                    strok = "#"
                answer = row[1]
                strok = re.sub(r"\s+", "", strok)
                row[1] = re.sub(r"\s+", "", row[1])
                #print(f'"{strok}"')
                #print(f'"{row[1]}"')
                #print()
                with open('1.csv', 'a', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow([image_name, strok, row[1], answer])
                error_wer = wer(row[1], strok)
                error_cer = cer(row[1], strok)
                #print(error_wer)
                sum_error_wer += error_wer
                sum_error_cer += error_cer
                if strok == row[1]:
                    right_answer_1 += 1

    end_time = datetime.datetime.now()
    execution_time = end_time - start_time

    #print('Чернобелое:')
    print('Библиотека: paddleocr en')
    print(f'Файл: {file_path}')
    print(f'Изменение изображения: чб; {filter}')
    print(f"Время выполнения программы: {execution_time}")
    print(f'{right_answer_1}/{current_number_file}')
    print(f'Вероятность верных ответов: {right_answer_1/(current_number_file)}')
    #print(sum_error_wer)
    print(f'WER = {sum_error_wer/(current_number_file)}')
    print(f'CER = {sum_error_cer / (current_number_file)}')
    print()
    print()
