import os
import csv
import cv2
import pytesseract
import datetime

limit = False
limitq = input('Введите количество изображений: ')

print(f'"{limitq}"')
if limitq != '':
    limit = True
    limitq = int(limitq)
else:
    limitq = 0
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
file_path = '1.csv'
images_folder_path = 'C:/Users/Mark/Downloads/dataset1/'

right_answer_1 = 0
current_number_file = 0

start_time = datetime.datetime.now()
if not os.path.isfile(file_path):
    print("Файла нет.")
else:
    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file)

        for row in csv_reader:
            current_number_file += 1
            if limit is True and limitq < current_number_file:
                break
            image_name = row[0]  # Предполагается, что имя файла находится в первом столбце (первая ячейка)
            image_path = os.path.join(images_folder_path, image_name)

            img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            strok = str(pytesseract.image_to_string(img,  config='--oem 3 --psm 6'))
            strok = strok.rstrip().rstrip('\n')
            if strok == row[1]:
                right_answer_1 += 1


end_time = datetime.datetime.now()
execution_time = end_time - start_time

print('Чернобелое:')
print(f"Время выполнения программы: {execution_time}")
print(right_answer_1)
print(current_number_file)
print(right_answer_1/current_number_file)


