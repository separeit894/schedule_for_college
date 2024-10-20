import os
import requests
from bs4 import BeautifulSoup

response = requests.get(url='https://vvfmtuci.ru/studentam/raspisanie-zanyatij-i-ekzamenov/spo/').text
soup = BeautifulSoup(response, "lxml")

directory_shedules = soup.find("div", class_='page__inner').find_all("p")

button_shedules = []
for directory in directory_shedules:
    if "неделя" in directory.text:
        button_shedules.append(directory.text)

print(button_shedules)
