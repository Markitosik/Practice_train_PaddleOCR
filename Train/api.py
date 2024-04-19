from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from PIL import Image
from io import BytesIO
import os
import subprocess
import re

app = FastAPI()
# Создаем папку для изображений, если она не существует
os.makedirs("images1", exist_ok=True)
# Определяем папку с изображениями как статическую папку
app.mount("/images1", StaticFiles(directory="images1"), name="images1")

html_form = """
<!DOCTYPE html>
<html>
<head>
    <title>Image Size Extractor</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        form {
            background-color: #fff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        h2 {
            text-align: center;
            color: #333;
            margin-bottom: 20px;
        }
        input[type="file"] {
            display: block;
            margin-bottom: 20px;
        }
        input[type="submit"] {
            background-color: #007bff;
            display: block;
            
            color: #fff;
            padding: 10px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            margin: auto;
        }
        input[type="submit"]:hover {
            background-color: #0056b3;
        }
        #response {
            margin-top: 20px;
            display: none;
        }
        .file-info {
            margin-top: 10px;
            font-size: 14px;
            text-align: center;
        }
    </style>
</head>
<body>
    <form id="upload-form" enctype="multipart/form-data" method="post">
        <h2>Upload Image</h2>
        <input type="file" id="file" name="file" accept="image/*">
        <input type="submit" value="Upload">
    </form>
    <div id="response" class="file-info">
        <!-- Здесь будет отображаться ответ API -->
        

    </div>
    <script>
        document.getElementById('upload-form').addEventListener('submit', async function(event) {
            event.preventDefault();
            const fileInput = document.getElementById('file');
            if (!fileInput.files[0]) {
                alert('Please select an image to upload.');
                return;
            }
            const formData = new FormData();
            formData.append('file', fileInput.files[0]);
            const response = await fetch('/upload/', {
                method: 'POST',
                body: formData
            });
            const data = await response.json();
            const responseDiv = document.getElementById('response');
            responseDiv.innerHTML = `</p><p>Filename: ${data.filename}</p>
                                    </p><p>Result: ${data.result}</p>
                                    <p>Width: ${data.width}</p>
                                    <p>Height: ${data.height}</p>`;
            responseDiv.style.display = 'block';  // Показываем блок с информацией о файле
        });
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def main():
    return HTMLResponse(content=html_form, status_code=200)

@app.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    if not file:
        return JSONResponse({"error": "No file uploaded"}, status_code=400)
    try:
        contents = await file.read()
        img = Image.open(BytesIO(contents))
        width, height = img.size
        #print(file)
        #print(contents)


        # Путь к папке изображений и полный путь к файлу
        folder_path = "images1"
        file_path = os.path.join(folder_path, file.filename)

        # Сохраняем файл на сервере
        with open(file_path, "wb") as f:
            f.write(contents)


        command = ('python ../PaddleOCR/tools/infer_rec.py  -c config3.yml ' +
                   '-o Global.checkpoints=output/rec/mark1.3/best_accuracy ' +
                   'Global.character_dict_path=../PaddleOCR/ppocr/utils/dict1.txt ' +
                   'Global.infer_img=./images1' + '\\' + file.filename)
        print(command)
        # Запускаем команду в терминале и получаем результат
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        print(result.stdout)
        pattern = r"result:\s+(\S+)"

        # Ищем первое совпадение с паттерном
        match = re.search(pattern, result.stdout)
        result = "'" + match.group(1) + "'"
        print(result)
        return JSONResponse({
            "filename": file.filename,
            "result": result,
            "width": width,
            "height": height
        })
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
