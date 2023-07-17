import requests
import json
from tkinter import *
from tkinter import ttk
from tkinter import font


def addtofav():
    filename = "fav.json"
    fav.append(city)
    for each in fav:
        each.upper()
    with open(filename, 'w') as file:
        json.dump(fav, file)
    weather_frame.config(highlightcolor="white")
    root.update()
    addfavbut.config(state="disabled", text="Added to favorites")


def get_data(a):
    global weather_frame, city, addfavbut, forecast
    try:
        response_API = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={a}&units=metric&APPID=391b09c375f6d5e144bdd9ace0d2273a")
        # print(response_API.status_code)
        data = response_API.text
        parse_json = json.loads(data)
        # print(parse_json)
        temp = parse_json['main']['temp']
        humidity = parse_json['main']['humidity']
        wind = int(parse_json['wind']['speed']) * (18 / 5)
        weather = parse_json['weather'][0]['main']
        city = parse_json['name']
        widgets = weather_frame.winfo_children()
        for widget in widgets:
            widget.destroy()
        temp_head = Label(weather_frame, text="Temperature: ", font=data_font, fg="grey")
        temp_head.grid(row=0, column=0)
        temp_label = Label(weather_frame, text=f"{temp} ℃", font=data_font)
        temp_label.grid(row=0, column=1)
        humidity_head = Label(weather_frame, text="Humidity: ", font=data_font, fg="grey")
        humidity_head.grid(row=1, column=0)
        humidity_label = Label(weather_frame, text=f"{humidity} %", font=data_font)
        humidity_label.grid(row=1, column=1)
        wind_head = Label(weather_frame, text="Wind: ", font=data_font, fg="grey")
        wind_head.grid(row=2, column=0)
        wind_label = Label(weather_frame, text=f"{wind} Km/hr", font=data_font)
        wind_label.grid(row=2, column=1)
        weather_head = Label(weather_frame, text="Weather: ", font=data_font, fg="grey")
        weather_head.grid(row=3, column=0)
        weather_label = Label(weather_frame, text=weather, font=data_font)
        weather_label.grid(row=3, column=1)
        city_head = Label(weather_frame, text="City: ", font=data_font, fg="grey")
        city_head.grid(row=4, column=0)
        city_label = Label(weather_frame, text=city, font=data_font)
        city_label.grid(row=4, column=1)
        forecast = ttk.Button(weather_frame, text="See Forecast", width=40, command=fetchforecast, state="enabled")
        forecast.grid(row=6, column=0, columnspan=2, ipady=5)
        addfavbut = ttk.Button(weather_frame, text="Add to favorites", width=40, command=addtofav)
        addfavbut.grid(row=5, column=0, columnspan=2, ipady=5)
        if city in fav:
            addfavbut.config(state="disabled", text="Added to favorites")
        else:
            addfavbut.config(state="enabled")

    except KeyError:
        widgets = weather_frame.winfo_children()
        for widget in widgets:
            widget.destroy()
        error = Label(weather_frame, text="City not found or some error occurred", font=data_font)
        error.grid(row=0, column=0)


def get_forecast_data(a):
    global weatherforecast_frame
    try:
        forecast.config(state="disabled")
        weather_frame.config(highlightcolor="white")
        response_API = requests.get(
            f"http://api.openweathermap.org/data/2.5/forecast?q={a}&units=metric&appid=391b09c375f6d5e144bdd9ace0d2273a")
        data = response_API.text
        parse_json = json.loads(data)
        i = 0
        widgets = forecast_frame.winfo_children()
        for widget in widgets:
            widget.destroy()
        # print(parse_json)
        for element in parse_json['list']:
            mcan.create_window(((root.winfo_width()) / 2.6, 0), window=sf, state="disabled", anchor=NW)
            mcan.bind('<Configure>', lambda e: mcan.config(scrollregion=mcan.bbox('all')))
            date = element['dt_txt']
            if "15:00:00" in str(date):
                subs = "15:00:00"
                temp = element['main']['temp']
                humidity = element['main']['humidity']
                wind = int(element['wind']['speed']) * (18 / 5)
                weather = element['weather'][0]['main']
                weatherforecast_frame = Frame(forecast_frame, highlightbackground="white", highlightthickness=4)
                weatherforecast_frame.pack(pady=(20, 10))
                date_head = Label(weatherforecast_frame, text=f"{str(date).replace(subs, '')}", font=data_font,
                                  fg="grey")
                date_head.grid(row=0, column=0 + i, columnspan=2)
                temp_head = Label(weatherforecast_frame, text="Temperature: ", font=data_font, fg="grey")
                temp_head.grid(row=1, column=0 + i)
                temp_label = Label(weatherforecast_frame, text=f"{temp} ℃", font=data_font)
                temp_label.grid(row=1, column=1 + i)
                humidity_head = Label(weatherforecast_frame, text="Humidity: ", font=data_font, fg="grey")
                humidity_head.grid(row=2, column=0 + i)
                humidity_label = Label(weatherforecast_frame, text=f"{humidity} %", font=data_font)
                humidity_label.grid(row=2, column=1 + i)
                wind_head = Label(weatherforecast_frame, text="Wind: ", font=data_font, fg="grey")
                wind_head.grid(row=3, column=0 + i)
                wind_label = Label(weatherforecast_frame, text=f"{wind} Km/hr", font=data_font)
                wind_label.grid(row=3, column=1 + i)
                weather_head = Label(weatherforecast_frame, text="Weather: ", font=data_font, fg="grey")
                weather_head.grid(row=4, column=0 + i)
                weather_label = Label(weatherforecast_frame, text=weather, font=data_font)
                weather_label.grid(row=4, column=1 + i)
                city_head = Label(weatherforecast_frame, text="City: ", font=data_font, fg="grey")
                city_head.grid(row=5, column=0+i)
                city_label = Label(weatherforecast_frame, text=city, font=data_font)
                city_label.grid(row=5, column=1+i)
                ghost = Frame(forecast_frame, width=20, height=10)
                ghost.pack()
                i += 1
            else:
                continue
        mcan.bind('<Configure>', lambda e: mcan.config(scrollregion=mcan.bbox('all')))

    except KeyError:
        print("City not found or some error occurred")


def fetchdata(self):
    get_data(loc.get())


def fetchforecast():
    get_forecast_data(loc.get())


def handle_selection(event):
    selected_item = combovar.get()
    loc.delete(0, END)
    loc.insert(0, selected_item)
    loc.focus_set()


def on_click(event):
    if combovar.get() == "Select from favorites":
        # Clear the text when clicked
        combovar.set("")


fav = []
with open("fav.json", 'r') as file:
    fav_list = json.load(file)
    for each in fav_list:
        fav.append(each)
root = Tk()
root.iconbitmap("weather.ico")
scw = root.winfo_screenwidth()
sch = root.winfo_screenheight()
root.geometry(f"{scw}x{sch}")
root.state('zoomed')
root.title('Weather')
root.resizable(False,True)
canva = Frame(root)
canva.pack(fill=BOTH, expand=1)
mcan = Canvas(canva)
mcan.pack(side=LEFT,fill=BOTH, expand=1)
scrbar = ttk.Scrollbar(canva, orient=VERTICAL, command=mcan.yview)
scrbar.pack(side=RIGHT, fill=Y)
mcan.config(yscrollcommand=scrbar.set)
mcan.bind('<Configure>', lambda e: mcan.config(scrollregion=mcan.bbox('all')))
sf = Frame(mcan)
mcan.create_window(((root.winfo_width())/2.6,0),window=sf,state="disabled",anchor=NW)
bold_font = font.Font(weight="bold", size=40, family="Arial Rounded MT Bold")
data_font = font.Font(family="Berlin Sans FB")
head = Label(sf, text="Check Weather", font=bold_font)
head.pack()
loc = ttk.Entry(sf, width=50, justify="center")
loc.pack(pady=(40, 30), ipady=5)
loc.bind("<Return>", fetchdata)
loc.focus_set()
frame = Frame(sf)
frame.pack()
combovar = StringVar()
combovar.set("Select from favorites")
select = ttk.Combobox(frame, width=37, values=fav, textvariable=combovar)
select.grid(row=0, column=0, ipady=5)
select.bind("<<ComboboxSelected>>", handle_selection)
select.bind("<Button-1>", on_click)
ghost = Frame(frame, width=20, height=10)
ghost.grid(row=1, column=0)
but = ttk.Button(frame, text="Check", width=40)
but.grid(row=2, column=0, ipady=5)
but.bind("<Button-1>", fetchdata)
weather_frame = Frame(sf, highlightbackground="white", highlightthickness=4)
weather_frame.pack(pady=(20, 10))
forecast_frame = Frame(sf)
forecast_frame.pack(pady=(20, 10))
root.mainloop()
