import os

for el in os.listdir("photo"):
    if "7 неделя СПО" in el:
        print("фото конвертирован")
        break
else:
    print("Нету таких фото")