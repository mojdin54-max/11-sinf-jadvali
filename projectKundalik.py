import asyncio
import os
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, FSInputFile, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart

# BotFather'дан олинган токенни шу ерга қўйинг
TOKEN = "8717230475:AAGKwQxqqfMhwVq8f1kG01AAOKKIpvxOu4c"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Ҳафта кунлари тугмалари (клавиатура)
keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Dushanba"), KeyboardButton(text="Seshanba")],
        [KeyboardButton(text="Chorshanba"), KeyboardButton(text="Payshanba")],
        [KeyboardButton(text="Juma"), KeyboardButton(text="Shanba")]
    ],
    resize_keyboard=True
)

# Kun nomlarini rasm nomlari bilan bog'lash
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
        "Assalomu alaykum! Dars jadvalini ko'rish uchun kerakli kunni tanlang:",
        reply_markup=keyboard
    )

# Тугма босилганда расмни юбориш
@dp.message(F.text.in_(DAYS_MAP.keys()))
async def send_schedule(message: Message):
    day_name = message.text
    image_file = DAYS_MAP[day_name]
    
    # 'img' папкаси ичидаги расмга йўл
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

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())