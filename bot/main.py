import asyncio
import httpx
from aiogram import Bot, Dispatcher
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from config import BOT_TOKEN, API_BASE

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

async def get_user(telegram_id: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_BASE}/users/me?telegram_id={telegram_id}")
        if response.status_code == 200:
            return response.json()
        return None

async def get_favorites(telegram_id: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_BASE}/favorites?telegram_id={telegram_id}")
        if response.status_code == 200:
            return response.json()
        return []

@dp.message(Command("start"))
async def start_handler(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Открыть СкидкоЛов", web_app={"url": "https://your-mini-app-url.com"})]  # Replace with actual URL
    ])
    await message.reply("Привет! Я бот СкидкоЛов. Нажимай кнопку, чтобы открыть приложение с скидками!", reply_markup=keyboard)

@dp.message(Command("favorites"))
async def favorites_handler(message: Message):
    telegram_id = str(message.from_user.id)
    user = await get_user(telegram_id)
    if not user:
        await message.reply("Сначала авторизуйся в Mini App!")
        return
    
    favorites = await get_favorites(telegram_id)
    if not favorites:
        await message.reply("У тебя нет избранных товаров.")
        return
    
    text = "Твои избранные товары:\n"
    for fav in favorites:
        text += f"- {fav['product_name']}: {fav['product_price']}₽\n"
    await message.reply(text)

# Add more handlers as needed

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())