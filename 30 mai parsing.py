import os
import sys
import requests
from tkinter import *
from PIL import Image, ImageTk
from tkinter.messagebox import showerror


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

#weather_condition = {"clear sky": "ясно", "broken clouds": "облачно с прояснениями",
                     #"rain": "дождь", "snow": "снег"}


def save_image(url):
    response = requests.get(url)
    with open(resource_path("weather_icon.png"), "wb") as file:
        file.write(response.content)
    image = Image.open(resource_path("weather_icon.png"))#перемещает временные файлы в папку
    return ImageTk.PhotoImage(image)


def show_weather():
    cityname = weather_entry.get()
    if not cityname:
        weather_info.config(text="")
        picture.config(image="", background="#F0F0F0")
        showerror("Ошибка", "Строка не может быть пустой")
    else:
        response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?"
                                f"q={cityname}&appid=3faa8133371792ef1aacd11949472dc8&lang=ru")
        if response.status_code != 404:
            response = response.json()

            img = save_image(f"https://openweathermap.org/img/wn/{response["weather"][0]["icon"]}@2x.png")
            picture.config(image=img, background="#0ceafa")
            picture.image = img
            weather_info.config(text=f"{(response["weather"][0]["description"]).capitalize()}\n"
                                f"Температура: {round(response["main"]["temp"] - 273.15)} C\n"
                                f"Скорость ветра: {response["wind"]["speed"]} м.с")
        else:
            weather_info.config(text="")#удаление текста при ошибке
            picture.config(image="", background="#F0F0F0")
            showerror("Ошибка", "Город не найден")


window = Tk()
window.geometry("500x500")
window.title("Прогноз погоды")
window.resizable(False, False)
window.iconbitmap("icon.ico")

welcome_text = Label(window, text="Прогноз погоды", font=("Time New Roman", 30, "bold"))
welcome_text.pack()

weather_entry = Entry(window)
weather_entry.pack(pady=10)
weather_entry.focus()

btn = Button(window, text="Показать погоду", command=show_weather)
btn.pack(pady=10)

picture = Label(window)
picture.pack()

weather_info = Label(window, font=("Time new Roman", 30, "bold"))
weather_info.pack()

window.mainloop()