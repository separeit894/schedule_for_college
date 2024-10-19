import os
import requests
import telebot
from telebot import types
from bs4 import BeautifulSoup
import fitz  # PyMuPDF
from PIL import Image

url = 'https://vvfmtuci.ru/studentam/raspisanie-zanyatij-i-ekzamenov/spo/'

bot = telebot.TeleBot(token='7471804498:AAFvG24hlMvOLr8XDTygBJGe4WgDOL8RnnQ')


@bot.message_handler(commands=['start'])
def main(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)

    response = requests.get(url=url).text
    soup = BeautifulSoup(response, "lxml")

    directory_shedules = soup.find("div", class_='page__inner').find_all("p")

    button_shedules = []
    for directory in directory_shedules:
        if "неделя" in directory.text:
            button_shedules.append(directory.text)

    for button in button_shedules:
        keyboard.add(button)

    bot.send_message(message.chat.id, "Привет, выберите неделю", reply_markup=keyboard)

    # Регистрируем следующий шаг
    bot.register_next_step_handler(message, test1)


def download_shedules(message):
    if "неделя" in message.text:
        bot.send_message(message.chat.id, f"Вы выбрали '<b>{message.text}</b>'", parse_mode="html")

        response = requests.get(url=url).text
        soup = BeautifulSoup(response, "lxml")

        directory_shedules = soup.find("div", class_='page__inner').find_all("p")
        for directory in directory_shedules:
            if message.text in directory.text:
                print(directory.text)
                result = 'https://vvfmtuci.ru/' + directory.find('a').get("href")

                try:
                    response_download = requests.get(result).content
                    bot.send_message(message.chat.id, "<b>Пожалуйста, подождите 20 секунд</b>", parse_mode="html")

                    # Создаем директорию, если она не существует
                    if not os.path.exists("shedules"):
                        os.makedirs("shedules")

                    else:
                        print("фыва")

                    if f"{directory.text}.pdf" in os.listdir("shedules"):
                        print("условие выполняется")

                    else:
                        with open(f"shedules/{message.text}.pdf", "wb") as file:
                            file.write(response_download)
                            # bot.send_message(message.chat.id, "файл download")

                        # Вызов функций конвертации и обрезки
                    path = "shedules"

                    # Открытие PDF

                    if not f"{directory.text}" in os.listdir("photo"):
                        print("проверка")
                        pdf_path = f"shedules/{directory.text}.pdf"
                        print(pdf_path)

                        pdf_document = fitz.open(pdf_path)
                        print(os.listdir(path))

                        # Конвертация каждой страницы в PNG
                        for page_number in range(len(pdf_document)):
                            page = pdf_document.load_page(page_number)  # Загружаем страницу
                            pix = page.get_pixmap()  # Получаем изображение страницы
                            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)  # Конвертируем в PIL Image
                            print(f"файл № {page_number} конвертирован")
                            img.save(f'photo/{directory.text}_{page_number}.png', 'PNG')  # Сохраняем как PNG

                        pdf_document.close()

                    for i in range(0, 14):
                        image = Image.open(f'photo/{directory.text}_{i}.png')

                        # Определите координаты для обрезки (left, upper, right, lower)
                        left = 50
                        upper = 100
                        right = 550
                        lower = 800

                        # Обрежьте изображение
                        cropped_image = image.crop((left, upper, right, lower))

                        # Сохраните обрезанное изображение
                        cropped_image.save(f'corrected_photo/page{i}.png')

                        print(f"Фото № {i} корректировано")



                    bot.send_message(message.chat.id, "Все выполнено")
                except Exception as e:
                    bot.send_message(message.chat.id, f"Произошла ошибка: {e}")
                    return


def test1(message):
    download_shedules(message)
    keyboards = types.ReplyKeyboardMarkup(resize_keyboard=True)
    groups = ["Р24", "Р24-11", "ИС24-1", "ИС24-2", "ОИБ24", "Р23", "Р23-11", "ИС23", "ОИБ23", "Р22-1", "Р22-2", "Р21-1",
              "Р21-2", "Р22-11"]
    for group in groups:
        keyboards.row(group)

    bot.send_message(message.chat.id, "Выберите свою группу", reply_markup=keyboards)

    bot.register_next_step_handler(message, result)

def result(message):
    if message.text == "Р24":
        with open("corrected_photo/page0.png", "rb") as file:
            src = file.read()
            bot.send_photo(message.chat.id, src)
    if message.text == "Р24-11":
        with open("corrected_photo/page1.png", "rb") as file:
            src = file.read()

            bot.send_photo(message.chat.id, src)
    if message.text == "ИС24-1":
        with open("corrected_photo/page2.png", "rb") as file:
            src = file.read()

            bot.send_photo(message.chat.id, src)
    if message.text == "ИС24-2":
        with open("corrected_photo/page3.png", "rb") as file:
            src = file.read()

            bot.send_photo(message.chat.id, src)
    if message.text == "ОИБ24":
        with open("corrected_photo/page4.png", "rb") as file:
            src = file.read()

            bot.send_photo(message.chat.id, src)
    if message.text == "Р23":
        with open("corrected_photo/page5.png", "rb") as file:
            src = file.read()

            bot.send_photo(message.chat.id, src)
    if message.text == "Р23-11":
        with open("corrected_photo/page6.png", "rb") as file:
            src = file.read()

            bot.send_photo(message.chat.id, src)
    if message.text == "ИС23":
        with open("corrected_photo/page7.png", "rb") as file:
            src = file.read()

            bot.send_photo(message.chat.id, src)

    if message.text == "ОИБ23":
        with open("corrected_photo/page8.png", "rb") as file:
            src = file.read()

            bot.send_photo(message.chat.id, src)
    if message.text == "Р22-1":
        with open("corrected_photo/page9.png", "rb") as file:
            src = file.read()

            bot.send_photo(message.chat.id, src)
    if message.text == "Р22-2":
        with open("corrected_photo/page10.png", "rb") as file:
            src = file.read()

            bot.send_photo(message.chat.id, src)
    if message.text == "Р21-1":
        with open("corrected_photo/page11.png", "rb") as file:
            src = file.read()

            bot.send_photo(message.chat.id, src)
    if message.text == "Р21-2":
        with open("corrected_photo/page12.png", "rb") as file:
            src = file.read()

            bot.send_photo(message.chat.id, src)
    if message.text == "Р22-11":
        with open("corrected_photo/page13.png", "rb") as file:
            src = file.read()

            bot.send_photo(message.chat.id, src)

    bot.send_message(message.chat.id, "<b>Для того чтобы выбрать другое неделю или группу\nВведите</b> /start", parse_mode="html")
    kback = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button_Yes = types.KeyboardButton("Да")
    button_No = types.KeyboardButton("Нет")
    kback.add(button_Yes, button_No)

    bot.send_message(message.chat.id, "Вы хотите выбрать другую группу?", reply_markup=kback)

    bot.register_next_step_handler(message, quest)

def quest(message):
    if message.text == "Нет":
        bot.send_message(message.chat.id, "Не доработано")
    if message.text == "Да":
        test1(message)


# Запуск бота
bot.polling(none_stop=True)