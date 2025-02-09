import requests
import json
import tkinter as tk
from tkinter import Label, Button
from PIL import Image, ImageTk
from io import BytesIO
from datetime import datetime, timezone, timedelta

def wind_dir(degrees):
    directions = ['Север', 'Северо-Восток', 'Восток', 'Юго-Восток'
                  , 'Юг', 'Юго-Запад', 'Запад', 'Северо-Запад']
    dir = round(degrees / 45) % 8
    return directions[dir]

def weather_soli(city):
    API_KEY = "a589f7636fe988bcb4d4a63494d33768"  #clave_API
    URL_WEATHER = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=ru"
    
    try:
        response = requests.get(URL_WEATHER)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Ошибка запроса к API: {e}")
        return None

def weather_data(data, city):
    if not data:
        return None
    
    try:
        weather_info = {
            "Город": city,
            "Описание": data['weather'][0]['description'],
            "Температура": f"{data['main']['temp']} °C",
            "Влажность": f"{data['main']['humidity']} %",
            "Давление": f"{data['main']['pressure']} hPa",
            "Скорость ветра": f"{data['wind']['speed']} м/с",
            "Направление ветра": wind_dir(data['wind']['deg']),
            "Координаты":{
                "Широта": f"{data['coord']['lat']}° N",
                "Долгота": f"{data['coord']['lon']}° E"},
            "Часовой пояс": f"UTC {data['timezone'] // 3600:+d}",
            "Местное время": (datetime.now(timezone.utc) + 
                              timedelta(seconds=data['timezone'])).strftime("%H:%M:%S"),
            "Местная дата": (datetime.now(timezone.utc) + 
                             timedelta(seconds=data['timezone'])).strftime("%Y-%m-%d")
        }
        return weather_info
    except KeyError as e:
        print(f"Ошибка обработки данных погоды: отсутствующий ключ {e}")
        return None

#Guardado en .json
def weather_json(weather_info, filename="weather.json"):
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(weather_info, file, ensure_ascii=False, indent=4)
            print(f"Данные сохранены в {filename}")
    except:
        print(f'Нет данных для сохранения :(')


def fox_image():
    FOX_URL = "https://randomfox.ca/floof/"
    response = requests.get(FOX_URL)
    if response.status_code == 200:
        fox_data = response.json()
        # print(fox_data)
        img_url = fox_data["image"]
        load_image(img_url)
        #print(img_url)
    else:
        print("Ошибка загрузки изображения")


def load_image(url):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    img = img.resize((420, 325), Image.Resampling.LANCZOS)
    img_tk = ImageTk.PhotoImage(img)
    fox_label.config(image=img_tk)
    fox_label.image = img_tk


if __name__ == "__main__":
    city = "Кито"  #Санкт-Петербург, Кито
    raw_data = weather_soli(city)
    parsed_data = weather_data(raw_data, city)
    weather_json(parsed_data)
    
    root = tk.Tk()
    root.title("Генератор лис")
    root.geometry("450x430")

    fox_label = Label(root)
    fox_label.pack()

    btn = Button(root, text="Сгенерировать новый", font=("Arial", 14), 
                 fg="darkgray", bg="blue", relief="raised", borderwidth=10, 
                 command=fox_image)
    btn.place(x=110, y=350)

    fox_image()
    root.mainloop()