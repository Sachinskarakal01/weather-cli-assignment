# weather_gui.py

import customtkinter as ctk
from tkinter import messagebox
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

from api_client import get_current_weather_by_city, get_forecast_by_city, APIError

# ---------- AUTO-CORRECT FEATURE ----------
from rapidfuzz import process

CITIES = [
    "London", "Mumbai", "Delhi", "New York", "Tokyo", "Paris",
    "Berlin", "Sydney", "Bangalore", "Pune", "Hyderabad",
    "Chennai", "Kolkata", "Dubai", "Singapore"
]

def autocorrect_city(city_name):
    city_name = city_name.strip()
    match = process.extractOne(city_name, CITIES, score_cutoff=60)
    if match:
        return match[0]
    return city_name
# ------------------------------------------


# App Theme
ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")


class WeatherApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Weather App - CustomTkinter")
        self.geometry("700x600")

        # Title
        self.label_title = ctk.CTkLabel(self, text="Weather App", font=("Arial", 28, "bold"))
        self.label_title.pack(pady=15)

        # City Input
        self.city_entry = ctk.CTkEntry(self, width=300, height=40, placeholder_text="Enter city name...")
        self.city_entry.pack(pady=10)

        # Buttons
        self.btn_frame = ctk.CTkFrame(self)
        self.btn_frame.pack(pady=10)

        self.btn_current = ctk.CTkButton(self.btn_frame, text="Current Weather", width=150,
                                         command=self.show_current_weather)
        self.btn_current.grid(row=0, column=0, padx=10)

        self.btn_forecast = ctk.CTkButton(self.btn_frame, text="5-Day Forecast", width=150,
                                          command=self.show_forecast)
        self.btn_forecast.grid(row=0, column=1, padx=10)

        # Output Box
        self.output_box = ctk.CTkTextbox(self, width=650, height=350, font=("Arial", 14))
        self.output_box.pack(pady=15)

    # ------------ CURRENT WEATHER ------------
    def show_current_weather(self):
        city = self.city_entry.get().strip()

        if city == "":
            messagebox.showwarning("Input Error", "Please enter a city name.")
            return

        # Apply Auto-correct
        city = autocorrect_city(city)

        try:
            data = get_current_weather_by_city(city)
            self.display_current_weather(data)
        except APIError as e:
            messagebox.showerror("Error", str(e))

    def display_current_weather(self, data):
        self.output_box.delete("0.0", "end")

        name = data.get("name", "N/A")
        country = data.get("sys", {}).get("country", "")
        weather = data.get("weather", [{}])[0]
        main = data.get("main", {})
        wind = data.get("wind", {})

        output = f"""
================ Current Weather ================
City: {name}, {country}
Condition: {weather.get('main')} - {weather.get('description')}

Temperature: {main.get('temp')} °C
Feels Like: {main.get('feels_like')} °C
Humidity: {main.get('humidity')} %
Pressure: {main.get('pressure')} hPa
Wind Speed: {wind.get('speed')} m/s
=================================================
"""
        self.output_box.insert("0.0", output)

    # ------------ FORECAST ------------
    def show_forecast(self):
        city = self.city_entry.get().strip()

        if city == "":
            messagebox.showwarning("Input Error", "Please enter a city name.")
            return

        # Apply Auto-correct
        city = autocorrect_city(city)

        try:
            data = get_forecast_by_city(city)
            self.display_forecast(data)
        except APIError as e:
            messagebox.showerror("Error", str(e))

    def display_forecast(self, data):
        self.output_box.delete("0.0", "end")

        output = "================ 5-Day / 3-Hour Forecast ================\n"
        for entry in data.get("list", [])[:12]:
            dt = entry.get("dt_txt", "")
            temp = entry.get("main", {}).get("temp", "")
            desc = entry.get("weather", [{}])[0].get("description", "")

            output += f"{dt}  |  {temp}°C  |  {desc}\n"

        output += "==========================================================\n"
        self.output_box.insert("0.0", output)


if __name__ == "__main__":
    app = WeatherApp()
    app.mainloop()
