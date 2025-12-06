# app.py
from dotenv import load_dotenv
load_dotenv()
import os
import click
from api_client import get_current_weather_by_city, get_forecast_by_city, APIError
from cache_manager import load, save, clear
from utils import print_current_weather, print_forecast_list, print_forecast_detail

load_dotenv()  # load .env if present

CACHE_AGE_MINUTES = 15

@click.group()
def cli():
    """Weather CLI — fetch current weather and 5-day forecast."""
    pass

@cli.command("list-current")
@click.argument("city")
@click.option("--refresh", is_flag=True, help="Force refresh from API (ignore cache).")
def list_current(city, refresh):
    """Show current weather for CITY"""
    key = f"current:{city.lower()}"
    data = None if refresh else load(key, max_age_minutes=CACHE_AGE_MINUTES)
    if not data:
        try:
            data = get_current_weather_by_city(city)
            save(key, data)
        except APIError as e:
            click.echo(f"[error] {e}")
            return
    print_current_weather(data)

@cli.command("list-forecast")
@click.argument("city")
@click.option("--limit", default=8, help="How many forecast entries to show (default 8).")
@click.option("--refresh", is_flag=True, help="Force refresh from API (ignore cache).")
def list_forecast(city, limit, refresh):
    """Show forecast list for CITY (5 day / 3 hour intervals)"""
    key = f"forecast:{city.lower()}"
    data = None if refresh else load(key, max_age_minutes=CACHE_AGE_MINUTES)
    if not data:
        try:
            data = get_forecast_by_city(city)
            save(key, data)
        except APIError as e:
            click.echo(f"[error] {e}")
            return
    print_forecast_list(data, limit)

@cli.command("show-forecast")
@click.argument("city")
@click.argument("index", type=int)
@click.option("--refresh", is_flag=True, help="Force refresh from API (ignore cache).")
def show_forecast(city, index, refresh):
    """Show detailed forecast entry by index (1-based)"""
    key = f"forecast:{city.lower()}"
    data = None if refresh else load(key, max_age_minutes=CACHE_AGE_MINUTES)
    if not data:
        try:
            data = get_forecast_by_city(city)
            save(key, data)
        except APIError as e:
            click.echo(f"[error] {e}")
            return
    print_forecast_detail(data, index)

@cli.command("clear-cache")
def do_clear_cache():
    """Clear local cache file"""
    clear()
    click.echo("Cache cleared.")

if __name__ == "__main__":
    cli()
