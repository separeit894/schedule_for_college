import os

import fitz  # PyMuPDF
from PIL import Image
path = "shedules"



def converter():
# Открытие PDF
    for el in os.listdir(path):
        pdf_path = f"shedules/{el}"
        print(el)

        pdf_document = fitz.open(pdf_path)
        print(os.listdir(path))

        # Конвертация каждой страницы в PNG
        for page_number in range(len(pdf_document)):
            page = pdf_document.load_page(page_number)  # Загружаем страницу
            pix = page.get_pixmap()  # Получаем изображение страницы
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)  # Конвертируем в PIL Image
            print(f"файл № {page_number} конвертирован")
            img.save(f'photo/page{page_number}.png', 'PNG')  # Сохраняем как PNG

        pdf_document.close()

converter()
