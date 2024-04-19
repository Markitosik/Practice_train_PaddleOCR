# Обучение нейросетей для распознования серийных номеров счетчиков водоснабжения в рамках производственной практики  
## Процесс разработки  
1. Была проведена разметка датасета подготовленных изображений счетчиков водоснабжения  
2. Составление статистике по нейросетям PaddleOCR и OCR Tesseract, применяя фильтры к изображениям, а также используя различные существующие предобученные модели  
3. Дообучение на нашем датасете англоязычной модели PaddleOCR и получение новой дообученной модели  
4. Создание API для распознования загружаемых изображений численнобуквенных серийных номеров  

## Применение  
### Дообучение:    
    python ../tools/train.py -c config3.yml -o Global.eval_batch_step=[0,200] Global.epoch_num=500 Global.pretrained_model=./output/rec/mark1.3/best_accuracy  

### Прогнозирование:  
    python ../tools/infer_rec.py -c config3.yml -o Global.checkpoints=output/rec/mark1.3/best_accuracy Global.character_dict_path=/ppocr/utils/dict1.txt Global.infer_img="путь к изображению или папке с изображениями"   

### Запуск:
    uvicorn api:app --reload 
![Запуск](https://github.com/Markitosik/Practice_train_PaddleOCR/blob/master/Train/%D0%97%D0%B0%D0%BF%D1%83%D1%81%D0%BA.png)

![Пример работы](https://github.com/Markitosik/Practice_train_PaddleOCR/blob/master/Train/%D0%A0%D0%B0%D0%B1%D0%BE%D1%82%D0%B0%20API%201.png)

    
