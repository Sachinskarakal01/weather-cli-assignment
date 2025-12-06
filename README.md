# 🌤️ Weather Application — Internship Assignment

A Python weather application built for the Global Trend Company internship assignment.  
The project interacts with the **OpenWeatherMap API** to retrieve weather data for any city in the world.

The application includes:
- Command Line Interface (CLI)
- Graphical User Interface (GUI)
- Auto-correction for wrong city names
- Error handling
- Clean and simple design

---

# 📝 Table of Contents
- Features
- Technologies Used
- Project Structure
- Requirements
- Installation
- API Key Setup
- Usage
- Auto-Correct Feature
- Error Handling
- Screenshots


---

# 🌟 Features

### ✅ Current Weather
Displays:
- Temperature
- Feels like
- Humidity
- Pressure
- Wind speed
- Weather condition

---

### ✅ 5-Day / 3-Hour Forecast
Provides weather forecast for 5 days in 3-hour steps.

---

### ✅ Auto-Correct City Names
Automatically fixes user spelling mistakes.

Example:


Londan → London
Mumbay → Mumbai
Delhii → Delhi


This is implemented using **RapidFuzz** fuzzy matching.

---

### ✅ GUI Version
Built using **CustomTkinter**, offering:
- Modern look
- Easy input
- Clean output display

---

# 🛠 Technologies Used
- Python
- OpenWeatherMap API
- requests
- python-dotenv
- customtkinter
- rapidfuzz
- JSON
- Git & GitHub

---

# 📁 Project Structure



weather_project/
│
├── app.py
├── weather_gui.py
├── api_client.py
├── utils.py
├── cache_manager.py
├── requirements.txt
├── README.md


---

# ✅ Requirements
- Python 3.10+
- Internet connection
- Free OpenWeatherMap API Key

---

# ⚙️ Installation

### 1️⃣ Clone the project
```sh
git clone https://github.com/yourusername/weather-project.git
cd weather-project

2️⃣ Create a virtual environment
python -m venv venv


Activate it:

Windows

venv\Scripts\activate


Mac/Linux

source venv/bin/activate

3️⃣ Install dependencies
pip install -r requirements.txt

🔑 API Key Setup

Create a .env file:

OWM_API_KEY=YOUR_API_KEY




🚀 Usage
🖥 CLI Version
Current Weather
python app.py list-current London

Forecast
python app.py list-forecast London

🪟 GUI Version

Run:

python weather_gui.py


A window will open where you can enter a city and get weather information.

🤖 Auto-Correct Feature

Even if users enter:

Sydny
Delhii
Mumbay


The program automatically corrects them to:

Sydney
Delhi
Mumbai

⚠️ Error Handling

The application handles:

Wrong city names

Missing API key

Empty input

Network failure

Unexpected API responses

Meaningful error messages are always shown.


# Screenshots

### GUI Screen
![GUI Screen](screenshots/GUI.png)

### Current Weather
![Current Weather](screenshots/current_weather.png)

### Forecast
![Forecast](screenshots/forecast.png)


