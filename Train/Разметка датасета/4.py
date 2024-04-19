import os
import tkinter as tk
import csv
from PIL import ImageTk, Image
import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

print("1 - Марк")
print("2 - Самвел")
print("3 - Аня")
print("4 - Артём")
print("5 - Аня(часть Артема)")
number = int(input("Введи свой номер: "))


def save_data(photo_path, number, comment):
    with open('data.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([photo_path, number, comment])

    with open('data.csv', mode='r') as file:
        # Создание объекта csv.reader для чтения CSV содержимого
        reader = csv.reader(file)

        # Подсчет количества строк
        row_count = sum(1 for row in reader)

    # Вывод количества строк
    print("Кол-во обработанных файлов:", row_count)


def iterate_photos(directory):
    photo_list = []
    global cont
    i = 0
    for filename in os.listdir(directory):
        if filename.endswith(".jpeg") or filename.endswith(".png"):
            if number == 1:
                if 0 <= i < 3178:
                    if last_photo == '':
                        cont = True
                    if cont is True:
                        photo_list.append(os.path.join(directory, filename))
                    if last_photo == filename:
                        cont = True
            if number == 2:
                if 1589 <= i < 4767:
                    if last_photo == '':
                        cont = True
                    if cont is True:
                        photo_list.append(os.path.join(directory, filename))
                    if last_photo == filename:
                        cont = True
            if number == 3:
                if i <= 3178 and i < 6356:
                    if last_photo == '':
                        cont = True
                    if cont is True:
                        photo_list.append(os.path.join(directory, filename))
                    else:
                        print('неа')
                    if last_photo == filename:
                        cont = True
            if number == 4:
                if 0 <= i < 1589 or 4767 < i <= 5700:
                    if last_photo == '':
                        cont = True
                    if cont is True:
                        photo_list.append(os.path.join(directory, filename))
                    if last_photo == filename:
                        cont = True
            if number == 5:
                if 5700 < i < 6356:
                    if last_photo == '':
                        cont = True
                    if cont is True:
                        photo_list.append(os.path.join(directory, filename))
                    if last_photo == filename:
                        cont = True

        i +=1
    return photo_list


def calculate_digit_percentage(string):
    digit_count = sum(1 for char in string if char.isdigit())
    total_characters = len(string)
    digit_percentage = 0
    if total_characters != 0:
        digit_percentage = (digit_count / total_characters) * 100

    return digit_percentage


def find_line_with_max_digit_percentage(new_line, max_percentage, max_percentage_line):
    percentage = calculate_digit_percentage(new_line)
    if percentage > max_percentage:
        max_percentage = percentage
        max_percentage_line = new_line

    return max_percentage_line, max_percentage


def display_photo():
    top_strok = ''
    max_percentage = 0
    top_strok = ''
    global current_index
    if current_index < len(photos):
        photo_path = photos[current_index]
        img = cv2.imread(photo_path, cv2.IMREAD_GRAYSCALE)

        imgs = {}
        for j in range(0, 10, 2):
            img1 = img
            img1 = img1[(j+1):(-j-1), :]
            height, width = img1.shape
            if height > 0 and width > 0:
                for i in range(5):
                    imgs[i] = cv2.resize(img1, None, fx=i + 1, fy=i + 1)
                    new_strok = str(pytesseract.image_to_string(imgs[i]))
                    print(new_strok.rstrip().rstrip('\n'))
                    if new_strok != "":
                        top_strok, max_percentage = find_line_with_max_digit_percentage(new_strok, max_percentage, top_strok)
            else:
                break

        strok = top_strok.rstrip().rstrip('\n').upper()
        number_entry.insert(0, strok)
        img = ImageTk.PhotoImage(Image.open(photo_path))
        image_label.config(image=img)
        image_label.photo = img
        current_index += 1
        return True
    else:
        image_label.config(text="Больше нет")
        return False


def next_photo():
    number = number_entry.get()
    comment = comment_entry.get()
    print(len(photos))
    print(current_index)
    save_data(os.path.basename(photos[current_index - 1]), number, comment)
    number_entry.delete(0, tk.END)
    comment_entry.delete(0, tk.END)
    next = display_photo()
    if next is False:
        exit()


def on_enter(event):
    # Вызовите функцию, связанную с кнопкой "Далее"
    next_photo()


last_photo = ''
cont = False

file_path = "data.csv"

# Проверка существования файла
if not os.path.isfile(file_path):
    print("Файла еще нет.")
else:
    # Открытие файла в режиме чтения
    with open(file_path, mode='r') as file:
        # Создание объекта csv.reader для чтения CSV содержимого
        reader = csv.reader(file)

        # Итерация по строкам в обратном порядке
        rows = list(reader)
        for row in reversed(rows):
            if any(row):
                # Вывод последней не пустой строки
                last_photo = row[0]
                print(last_photo)
                break
        else:
            # Если все строки пустые
            print("Файл пуст.")

# Инициализация Tkinter
window = tk.Tk()
window.title("Photo Viewer")

# Отображение фото
image_label = tk.Label(window)
image_label.pack()

# Поле ввода номера
number_label = tk.Label(window, text="Value:")
number_label.pack()

number_entry = tk.Entry(window, width=40)
number_entry.pack()

comment_label = tk.Label(window, text="Comment:")
comment_label.pack()

comment_entry = tk.Entry(window, width=40)
comment_entry.pack()

# Кнопка "Далее"
next_button = tk.Button(window, text="Next", command=next_photo)
next_button.pack()

# Привязка события нажатия клавиши Enter к функции on_enter
window.bind('<Return>', on_enter)

# Получение списка фотографий
directory = "C:/Users/Mark/Downloads/dataset1/"
photos = iterate_photos(directory)
current_index = 0

# Отображение первого фото
display_photo()

# Запуск Tkinter
window.mainloop()
