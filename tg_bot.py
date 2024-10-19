import requests
import telebot
from telebot import types
from bs4 import BeautifulSoup
from cropped_photos import cropped
from pdf_converter_to_png import converter
import os
import logging

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
                result = 'https://vvfmtuci.ru/' + directory.find('a').get("href")

                try:
                    response_download = requests.get(result).content
                    bot.send_message(message.chat.id, "<b>Пожалуйста, подождите 20 секунд</b>", parse_mode="html")

                    # Создаем директорию, если она не существует
                    if not os.path.exists("shedules"):
                        os.makedirs("shedules")

                    with open(f"shedules/{message.text}.pdf", "wb") as file:
                        file.write(response_download)

                    # Вызов функций конвертации и обрезки
                    convert = converter()
                    print(convert)
                    cropp = cropped()
                    print(cropp)

                    bot.send_message(message.chat.id, "Все выполнено")
                except Exception as e:
                    bot.send_message(message.chat.id, f"Произошла ошибка: {e}")
                    return

        # Регистрируем следующий шаг
        # bot.register_next_step_handler(message, test1)


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


# Запуск бота
bot.polling(none_stop=True)
