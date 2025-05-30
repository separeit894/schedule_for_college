import os, time
import requests
import telebot
from telebot import types
from bs4 import BeautifulSoup
from PIL import Image
from dotenv import load_dotenv
from pdf2image import convert_from_path
import threading
from datetime import datetime
load_dotenv()

# Список для хранения идентификаторов чатов
chat_ids = []

url = 'https://vvfmtuci.ru/studentam/raspisanie-zanyatij-i-ekzamenov/spo/'

bot = telebot.TeleBot(token=os.getenv("TOKEN"))


if not os.path.exists("shedules"):
    os.makedirs("shedules")

if not os.path.exists("photo"):
    os.makedirs("photo")

if not os.path.exists("corrected_photo"):
    os.makedirs("corrected_photo")

@bot.message_handler(commands=['start'])
def main(message):
    chat_ids.append(message.chat.id)

    bot.send_message(message.chat.id, "<b>Сброс бота происходит в полночь по московскому времени!</b>", parse_mode="html")

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

    bot.send_message(message.chat.id, "Здравствуйте, выберите неделю: ", reply_markup=keyboard)

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
                result_link = 'https://vvfmtuci.ru/' + directory.find('a').get("href")

                try:
                    response_download = requests.get(result_link).content
                    bot.send_message(message.chat.id, "<b>Пожалуйста, подождите 10-20 секунд</b>", parse_mode="html")


                    if f"{directory.text}.pdf" in os.listdir("shedules"):
                        print(f"{directory.text}.pdf есть в директории")

                    else:
                        with open(f"shedules/{message.text}.pdf", "wb") as file:
                            file.write(response_download)
                        print(f"Файл '{message.text}' загружен")


                    # Открытие и конвертация pdf в png файлы

                    for el in os.listdir("photo"):
                        if f"{message.text}" in el:
                            print("Конвертированные фотографии этого расписания присутствуют")
                            break
                    else:
                        pdf_path = f"shedules/{directory.text}.pdf"

                        images = convert_from_path(pdf_path)
                        for i, image in enumerate(images):
                            image.save(f"photo/{directory.text}_{i}.png", "PNG")
                            print(f"файл № {i} конвертирован")
                        print("Файлы конвертированы")

                    # Обрезка фотографий
                    for i in range(0, 14):
                        image = Image.open(f'photo/{directory.text}_{i}.png')

                        # Определите координаты для обрезки (left, upper, right, lower)
                        left = 100
                        upper = 300
                        right = 1500
                        lower = 2100

                        # Обрежьте изображение
                        cropped_image = image.crop((left, upper, right, lower))

                        # Сохраните обрезанное изображение
                        cropped_image.save(f'corrected_photo/{message.from_user.username}_page{i}.png')

                        print(f"Фото № {i} корректировано")

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
        with open(f"corrected_photo/{message.from_user.username}_page0.png", "rb") as file:
            src = file.read()
            bot.send_photo(message.chat.id, src)
    if message.text == "Р24-11":
        with open(f"corrected_photo/{message.from_user.username}_page1.png", "rb") as file:
            src = file.read()

            bot.send_photo(message.chat.id, src)
    if message.text == "ИС24-1":
        with open(f"corrected_photo/{message.from_user.username}_page2.png", "rb") as file:
            src = file.read()

            bot.send_photo(message.chat.id, src)
    if message.text == "ИС24-2":
        with open(f"corrected_photo/{message.from_user.username}_page3.png", "rb") as file:
            src = file.read()

            bot.send_photo(message.chat.id, src)
    if message.text == "ОИБ24":
        with open(f"corrected_photo/{message.from_user.username}_page4.png", "rb") as file:
            src = file.read()

            bot.send_photo(message.chat.id, src)
    if message.text == "Р23":
        with open(f"corrected_photo/{message.from_user.username}_page5.png", "rb") as file:
            src = file.read()

            bot.send_photo(message.chat.id, src)
    if message.text == "Р23-11":
        with open(f"corrected_photo/{message.from_user.username}_page6.png", "rb") as file:
            src = file.read()

            bot.send_photo(message.chat.id, src)
    if message.text == "ИС23":
        with open(f"corrected_photo/{message.from_user.username}_page7.png", "rb") as file:
            src = file.read()

            bot.send_photo(message.chat.id, src)

    if message.text == "ОИБ23":
        with open(f"corrected_photo/{message.from_user.username}_page8.png", "rb") as file:
            src = file.read()

            bot.send_photo(message.chat.id, src)
    if message.text == "Р22-1":
        with open(f"corrected_photo/{message.from_user.username}_page9.png", "rb") as file:
            src = file.read()

            bot.send_photo(message.chat.id, src)
    if message.text == "Р22-2":
        with open(f"corrected_photo/{message.from_user.username}_page10.png", "rb") as file:
            src = file.read()

            bot.send_photo(message.chat.id, src)
    if message.text == "Р21-1":
        with open(f"corrected_photo/{message.from_user.username}_page11.png", "rb") as file:
            src = file.read()

            bot.send_photo(message.chat.id, src)
    if message.text == "Р21-2":
        with open(f"corrected_photo/{message.from_user.username}_page12.png", "rb") as file:
            src = file.read()

            bot.send_photo(message.chat.id, src)
    if message.text == "Р22-11":
        with open(f"corrected_photo/{message.from_user.username}_page13.png", "rb") as file:
            src = file.read()

            bot.send_photo(message.chat.id, src)

    bot.send_message(message.chat.id, "<b>Для того чтобы выбрать другую неделю.\nВведите</b> /start",
                     parse_mode="html")
    keyboard_back = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button_yes = types.KeyboardButton("Да")
    button_no = types.KeyboardButton("Нет")
    keyboard_back.add(button_yes, button_no)

    bot.send_message(message.chat.id, "Вы хотите выбрать другую группу?", reply_markup=keyboard_back)

    bot.register_next_step_handler(message, quest)

def quest(message):
    if message.text == "Нет":
        directory_path = 'corrected_photo'

        # Удаляем все файлы в директории
        for filename in os.listdir(directory_path):
            if f"{message.from_user.username}" in filename:
                file_path = os.path.join(directory_path, filename)
                if os.path.isfile(file_path):  # Проверяем, что это файл
                    os.remove(file_path)
                    print(f'Файл {file_path} удалён.')
        bot.send_message(message.chat.id, "<b>Для того чтобы выбрать другую неделю.\nВведите</b> /start", parse_mode="html")
    if message.text == "Да":
        test1(message)


# пока что в доработке
@bot.message_handler(commands=['reset'])
def private_reset(message):
    # Удаление файлов с расписаниями
    directory_path = 'shedules'

    # Удаляем все файлы в директории
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        if os.path.isfile(file_path):  # Проверяем, что это файл
            os.remove(file_path)
            print(f'Файл {file_path} удалён.')

    bot.send_message(message.chat.id, "Файлы расписаний удалены")

    # Удаление все конвертированных png
    directory_path = 'photo'

    # Удаляем все файлы в директории
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        if os.path.isfile(file_path):  # Проверяем, что это файл
            os.remove(file_path)
            print(f'Файл {file_path} удалён.')

    bot.send_message(message.chat.id, "Конвертированные png удалены")

    # Удаление корректрированныe png
    directory_path = 'corrected_photo'

    # Удаляем все файлы в директории
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        if os.path.isfile(file_path):  # Проверяем, что это файл
            os.remove(file_path)
            print(f'Файл {file_path} удалён.')

    bot.send_message(message.chat.id, "Корректированные файлы удалены")

def auto_reset():

    # Получаем текущее время
    while True:
        now = datetime.now()
        print(now)

        # Проверяем, если текущее время 23:00
        if now.hour == 23 and now.minute == 54 and now.second == 50:
            print("Время наступило")

        if now.hour == 0 and now.minute == 0 and now.second == 0:
            print("Время наступило")
            # Удаление файлов с расписаниями
            directory_path = 'shedules'

            # Удаляем все файлы в директории
            for filename in os.listdir(directory_path):
                file_path = os.path.join(directory_path, filename)
                if os.path.isfile(file_path):  # Проверяем, что это файл
                    os.remove(file_path)
                    print(f'Файл {file_path} удалён.')

            print("файлы с расписаниями удалены")
            # Удаление все конвертированных png
            directory_path = 'photo'

            # Удаляем все файлы в директории
            for filename in os.listdir(directory_path):
                file_path = os.path.join(directory_path, filename)
                if os.path.isfile(file_path):  # Проверяем, что это файл
                    os.remove(file_path)
                    print(f'Файл {file_path} удалён.')

            print("png удалены")


            # Удаление корректрированныe png
            directory_path = 'corrected_photo'

            # Удаляем все файлы в директории
            for filename in os.listdir(directory_path):
                file_path = os.path.join(directory_path, filename)
                if os.path.isfile(file_path):  # Проверяем, что это файл
                    os.remove(file_path)
                    print(f'Файл {file_path} удалён.')

            print("корректированные png удалены")
            for chat_id in chat_ids:
                bot.send_message(chat_id, "Произошел reset бота")
            # Ждем 60 секунд, чтобы избежать многократного вывода
            time.sleep(60)

        time.sleep(1)



threading.Thread(target=auto_reset, daemon=True).start()


# Запуск бота
bot.polling(none_stop=True)