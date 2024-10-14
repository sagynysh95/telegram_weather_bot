import asyncio

from aiogram import Bot, types, Dispatcher
from aiogram.filters import CommandStart
import requests
from datetime import datetime

from config import BOT_TOKEN, WEATHER_TOKEN


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot=bot)


@dp.message(CommandStart())
async def start_command(message: types.Message):
    await message.answer('Привет, напиши название города')


@dp.message()
async def weather_func(message: types.Message):
    try:
        r = requests.get(
            f"http://api.openweathermap.org/geo/1.0/direct?q={message.text}&appid={WEATHER_TOKEN}"
        ) # to get lat and lon
        data = r.json()
        lat = data[0]['lat']
        lon = data[0]['lon']
        r1 = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={WEATHER_TOKEN}&units=metric"
        )
        data1 = r1.json()
        city_name = data1['name']
        temp = data1['main']['temp']
        humidity = data1['main']['humidity']
        wind = data1['wind']['speed']

        await message.answer(f'***{datetime.now().strftime("%Y-%m-%d %H:%M")}***\n'
                             f'City: {city_name}\nTemperature: {temp}°C\n'
                             f'Humidity: {humidity}%\nWind: {wind} m/s')
    except Exception as ex:
        await message.answer('Try again')


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())