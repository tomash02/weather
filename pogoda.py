#!/usr/bin/python

from urllib.request import urlopen
from urllib.error import HTTPError
from tkinter import messagebox
import urllib.parse
import tkinter as tk
import json
from datetime import date, datetime
from PIL import ImageTk, Image
from io import BytesIO

weather_Dict = {
    "dayOne": "",
    "dayTwo": "",
    "dayThree": "",
    "dayFour": "",
    "dayFive": "",
}

data = {}
key = "1c3a6625bc4e93cf967881614b2c52c4"
lang = "pl"


def kelvin_to_farenheit_conversion(temperature):
    converted = (temperature)
    #(temperature * 9/5) + 32
    return int(converted)

def show_temp(gr, temp):
    label = tk.Label(
        master=root, text=f"Temperatura wynosi {temp}°C", padx=10, bg='grey'
    )
    label.grid(row=gr, column=0, columnspan=6)

def label_icon(gr, conditions, iconID):
    iconUrl = f'http://openweathermap.org/img/wn/{iconID}@2x.png'
    u = urlopen(iconUrl)
    raw = u.read()
    u.close()
    img = Image.open(BytesIO(raw))
    photo = ImageTk.PhotoImage(img)
    icon = tk.Label(image=photo, bg='grey')
    icon.image = photo
    icon.grid(row=gr, column=0, columnspan=6)
    descript_label = tk.Label(
        master=root, text=conditions.capitalize(), padx=6, bg='grey'
    )
    descript_label.grid(row=gr+2, column=0, columnspan=6)

def date_to_day(gr, num):
    date_object = datetime.strptime(weather_Dict[f'day{num}']['dt_txt'], '%Y-%m-%d %H:%M:%S')
    weekday_label = tk.Label(
        master=root, text=date_object.strftime("%A %d.%m"), padx=10, bg='grey', font=("bold", 14)
    )
    weekday_label.grid(row=gr, column=0, columnspan=6)

def populate_weather(city_name):
    url_encoded_city_name = urllib.parse.quote(city_name)
    try:
        url = f"http://api.openweathermap.org/data/2.5/forecast?q={url_encoded_city_name}&appid={key}&lang={lang}&units=metric"
        with urlopen(url) as response:
            source = response.read()
    except HTTPError:
        tk.messagebox.showwarning(
            title="Błąd!!!", message="Sprawdź nazwę miasta!"
        )
    except Exception as e:
        tk.messagebox.showwarning(title="Uwaga!", message=f"Nieznany błąd! {e}")

    else:
        data = json.loads(source)

        weather_Dict["dayOne"] = data["list"][0]
        weather_Dict["dayTwo"] = data["list"][8]
        weather_Dict["dayThree"] = data["list"][16]
        weather_Dict["dayFour"] = data["list"][24]
        weather_Dict["dayFive"] = data["list"][32]
        # dzień1
        date_to_day(4, 'One')
        label_icon(5, weather_Dict['dayOne']['weather'][0]['description'], weather_Dict['dayOne']['weather'][0]['icon'])
        show_temp(6, int(weather_Dict['dayOne']['main']['temp']))
        # dzień2
        date_to_day(8, 'Two')
        label_icon(9, weather_Dict['dayTwo']['weather'][0]['description'], weather_Dict['dayTwo']['weather'][0]['icon'])
        show_temp(10, int(weather_Dict['dayTwo']['main']['temp']))
        # dzień3
        date_to_day(12, 'Three')
        label_icon(13, weather_Dict['dayThree']['weather'][0]['description'], weather_Dict['dayThree']['weather'][0]['icon'])
        show_temp(14, int(weather_Dict['dayThree']['main']['temp']))
        #dzień4
        date_to_day(16, 'Four')
        label_icon(17, weather_Dict['dayFour']['weather'][0]['description'], weather_Dict['dayFour']['weather'][0]['icon'])
        show_temp(18, int(weather_Dict['dayFour']['main']['temp']))
        #dzień5
        date_to_day(20, 'Five')
        label_icon(21, weather_Dict['dayFive']['weather'][0]['description'], weather_Dict['dayFive']['weather'][0]['icon'])
        show_temp(22, int(weather_Dict['dayFive']['main']['temp']))




def get_weather():
    city_name = city_text.get()
    populate_weather(city_name)


# GUI
root = tk.Tk()
root.title("Pogodynka v.0.5")
root.geometry("400x900")
root.configure(bg='grey')
city_text = tk.StringVar()
city_label = tk.Label(root, text="Nazwa miasta", font=("bold", 14), padx=10, bg='grey')
city_label.grid(row=2,column=2)
city_entry = tk.Entry(root, textvariable=city_text)
city_entry.grid(row=2,column=3)
weather_btn = tk.Button(root, text="Pobierz prognozę", width=12, command=get_weather, bg='grey')
weather_btn.grid(row=2,column=5)
root.mainloop()
