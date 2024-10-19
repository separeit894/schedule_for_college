import os

import requests
from bs4 import BeautifulSoup

def main(url):

    response = requests.get(url).text
    soup = BeautifulSoup(response, "lxml")

    directory_shedules = soup.find("div", class_='page__inner').find_all("p")
    i = 0
    for directory in directory_shedules:
        if "неделя" in directory.text:
            result = 'https://vvfmtuci.ru/' + directory.find('a').get("href")

            response_download = requests.get(result).content

            with open(f"shedules/{directory.text}.pdf", "wb") as file:
                i += 1
                file.write(response_download)

            break



if __name__ == "__main__":
    main('https://vvfmtuci.ru/studentam/raspisanie-zanyatij-i-ekzamenov/spo/')