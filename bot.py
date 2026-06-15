import os
import json
import logging
import asyncio
import aiohttp
import xml.etree.ElementTree as ET
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.client.session.aiohttp import AiohttpSession
# настройки бота
TOKEN = os.getenv("TOKEN", "Token")  # токен бота
LOWER_BOUND = 70.0  # нижняя граница курса
UPPER_BOUND = 85.0  # верхняя граница курса
ADMIN_IDS = [1540008988]  # id админа
DATA_FILE = "exchange_data.json"  # файл для хранения
logging.basicConfig(level=logging.INFO)
session = AiohttpSession()
dp = Dispatcher()
bot = Bot(token=TOKEN, session=session)
# загрузка списка
def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return {"subscribers": []}  # если файла нет, создаём пустой список
# сохранение списка в файл
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)
# парсинг курса доллара с сайта цб рф
async def get_usd_rate():
    try:
        async with aiohttp.ClientSession() as sess:
            async with sess.get("https://www.cbr.ru/scripts/XML_daily.asp", timeout=10) as resp:
                root = ET.fromstring(await resp.text())
                for valute in root.findall('Valute'):
                    if valute.find('CharCode').text == 'USD':  # ищем доллар
                        return float(valute.find('Value').text.replace(',', '.'))  # преобразуем в число
    except Exception as e:
        logging.error(f"Ошибка: {e}")
    return None  # если ошибка - возвращаем None
# команда /start
@dp.message(Command("start"))
async def start(msg: Message):
    # автоматическая подписка пользователя на уведомления об изменении курса
    data = load_data()
    if msg.from_user.id not in data["subscribers"]:
        data["subscribers"].append(msg.from_user.id)
        save_data(data)
    await msg.answer(
        f"Текущие границы: {LOWER_BOUND} - {UPPER_BOUND} ₽\n\n"
        f"Команды:\n"
        f"/rate - узнать текущий курс\n"
        f"/set_bounds 70 85 - изменить границы (админ)"
    )
# команда /rate - показать текущий курс
@dp.message(Command("rate"))
async def rate(msg: Message):
    rate = await get_usd_rate()
    if rate:
        warning = ""
        if rate < LOWER_BOUND:
            warning = f"\nКурс ниже границы ({LOWER_BOUND} ₽)!"
        elif rate > UPPER_BOUND:
            warning = f"\nКурс выше границы ({UPPER_BOUND} ₽)!"

        await msg.answer(f"Курс USD: {rate} ₽{warning}")
    else:
        await msg.answer("Ошибка")
# команда /set_bounds - изменить границы (только для админа)
@dp.message(Command("set_bounds"))
async def set_bounds(msg: Message):
    # проверка, что только админ может менять границы
    if msg.from_user.id not in ADMIN_IDS:
        await msg.answer("Нет прав")
        return
    try:
        _, low, up = msg.text.split()  # команда /set_bounds 70 85
        global LOWER_BOUND, UPPER_BOUND
        LOWER_BOUND = float(low)
        UPPER_BOUND = float(up)
        await msg.answer(f"Границы обновлены: {LOWER_BOUND} - {UPPER_BOUND} ₽")
    except:
        await msg.answer("Пример: /set_bounds 70 85")
# проверка курса каждые 5 минут
async def periodic_check():
    while True:
        rate = await get_usd_rate()
        # если курс вышел за границы,то рассылаем уведомление
        if rate and (rate < LOWER_BOUND or rate > UPPER_BOUND):
            data = load_data()
            for user_id in data["subscribers"]:
                try:
                    await bot.send_message(
                        user_id,
                        f"УВЕДОМЛЕНИЕ!\n\n"
                        f"Курс USD: {rate} ₽\n"
                        f"Выход за границы ({LOWER_BOUND} - {UPPER_BOUND} ₽)"
                    )
                except:
                    pass  # если не отправилось, то пропуск
        await asyncio.sleep(300)  # пауза 5 минут
# главная функция
async def main():
    asyncio.create_task(periodic_check())  # запускаем фоновую проверку курса
    await dp.start_polling(bot)  # запускаем бота
if __name__ == "__main__":
    asyncio.run(main())