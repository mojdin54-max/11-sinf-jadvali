import asyncio
import os
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, FSInputFile, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart, Command
from aiohttp import web

# ЗАМЕНИТЕ ЭТОТ ТОКЕН! Получите новый через @BotFather -> /revoke
TOKEN = "8717230475:AAHucrGEeKfmFJW3MdhBiIqIiU_9SOdyIyM"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Klaviatura
keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Dushanba"), KeyboardButton(text="Seshanba")],
        [KeyboardButton(text="Chorshanba"), KeyboardButton(text="Payshanba")],
        [KeyboardButton(text="Juma"), KeyboardButton(text="Shanba")]
    ],
    resize_keyboard=True
)

# Fayllar xaritasi
DAYS_MAP = {
    "Dushanba": "dushanba.jpg",
    "Seshanba": "seshanba.jpg",
    "Chorshanba": "chorshanba.jpg",
    "Payshanba": "payshanba.jpg",
    "Juma": "juma.jpg",
    "Shanba": "shanba.jpg"
}

@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        "Assalomu alaykum! Dars jadvalini ko'rish uchun kerakli kunni tanlang yoki buyruq yuboring (masalan: /dushanba):",
        reply_markup=keyboard
    )

@dp.message(F.text.in_(DAYS_MAP.keys()))
@dp.message(Command(commands=["dushanba", "seshanba", "chorshanba", "payshanba", "juma", "shanba"]))
async def send_schedule(message: Message):
    if message.text.startswith('/'):
        raw_cmd = message.text.split('@')[0].replace('/', '')
        day_name = raw_cmd.capitalize()
    else:
        day_name = message.text

    if day_name in DAYS_MAP:
        image_file = DAYS_MAP[day_name]
        photo_path = os.path.join("img", image_file)
        
        if os.path.exists(photo_path):
            photo = FSInputFile(photo_path)
            await message.answer_photo(
                photo=photo,
                caption=f"📌 **{day_name} kungi dars jadvali**",
                parse_mode="Markdown"
            )
        else:
            await message.answer(f"⚠️ {day_name} kuni uchun rasm topilmadi! (`img/{image_file}` faylini tekshiring)")

# Веб-сервер заглушка для Render Web Service
async def handle(request):
    return web.Response(text="Bot runs 24/7!")

async def start_web_server():
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.ApplicationRunner if hasattr(web, 'ApplicationRunner') else web.AppRunner
    r = runner(app)
    await r.setup()
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(r, "0.0.0.0", port)
    await site.start()

async def main():
    await start_web_server()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
