# utils.py
from typing import Dict, Any, List
from rich.table import Table
from rich.console import Console

console = Console()

def print_current_weather(data: Dict[str, Any]):
    """
    Nicely print current weather JSON from OpenWeatherMap.
    """
    if not data:
        console.print("[red]No data to display[/red]")
        return

    name = data.get("name", "N/A")
    sys = data.get("sys", {})
    country = sys.get("country", "")
    weather = data.get("weather", [{}])[0]
    main = data.get("main", {})
    wind = data.get("wind", {})

    console.print(f"[bold cyan]{name}, {country}[/bold cyan]")
    console.print(f"[bold]{weather.get('main', 'N/A')}[/bold] - {weather.get('description','')}")
    console.print(f"Temperature: {main.get('temp','N/A')}°C (feels like {main.get('feels_like','N/A')}°C)")
    console.print(f"Humidity: {main.get('humidity','N/A')}%")
    console.print(f"Pressure: {main.get('pressure','N/A')} hPa")
    console.print(f"Wind: {wind.get('speed','N/A')} m/s")

def print_forecast_list(forecast_data: Dict[str, Any], limit: int = 10):
    """
    Print a tabular forecast (time, temp, weather).
    Limit controls number of entries to display.
    """
    if not forecast_data:
        console.print("[red]No forecast data to display[/red]")
        return

    entries = forecast_data.get("list", [])
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Index", width=6)
    table.add_column("DateTime", width=20)
    table.add_column("Temp (°C)", justify="right")
    table.add_column("Weather")

    for i, e in enumerate(entries[:limit], start=1):
        dt = e.get("dt_txt", "N/A")
        temp = e.get("main", {}).get("temp", "N/A")
        weather = e.get("weather", [{}])[0].get("description", "")
        table.add_row(str(i), dt, str(temp), weather)

    console.print(table)

def print_forecast_detail(forecast_data: Dict[str, Any], index: int):
    entries = forecast_data.get("list", [])
    if index < 1 or index > len(entries):
        console.print(f"[red]Index out of range. Provide index between 1 and {len(entries)}[/red]")
        return
    e = entries[index - 1]
    dt = e.get("dt_txt", "N/A")
    main = e.get("main", {})
    weather = e.get("weather", [{}])[0]
    wind = e.get("wind", {})
    console.print(f"[bold]Forecast for {dt}[/bold]")
    console.print(f"Temp: {main.get('temp','N/A')}°C (min {main.get('temp_min','N/A')}, max {main.get('temp_max','N/A')})")
    console.print(f"Weather: {weather.get('main','N/A')} - {weather.get('description','')}")
    console.print(f"Humidity: {main.get('humidity','N/A')}%")
    console.print(f"Pressure: {main.get('pressure','N/A')} hPa")
    console.print(f"Wind: {wind.get('speed','N/A')} m/s")
