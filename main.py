import logging
import os

from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import BotCommand
from dotenv import load_dotenv

from data_download import world_music, main_data, top_music, new_trek, check_user, register, get_user, create_table
from inline_btns import main_btn, world_track, top_track
from reply_btns import start_btn, admin_page

load_dotenv('.env')

BOT_TOKEN = os.getenv('TOKEN')
bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

logging.basicConfig(level=logging.INFO)


class ReklamaState(StatesGroup):
    reklama = State()


class ReqState(StatesGroup):
    fikrlar = State()


@dp.message_handler(commands='start')
async def start_handler(msg: types.Message):
    await bot.set_my_commands([BotCommand('start', "Qayta ishga tushirish"), BotCommand('help', 'Yordam olish')])
    if not check_user(str(msg.from_user.id)):
        user = msg.from_user
        register(str(user.id))
    await msg.answer(
        text="Assalomu alaykum 🤖\nBotimizga xush kelibsiz 😊\nBot sinov holatida ishlamoqda ⏳\nBot haqida talab va takliflar uchun adminga murojat qiling 👨🏻‍💻",
        reply_markup=start_btn())


@dp.message_handler(commands='help')
async def help_handler(msg: types.Message):
    await msg.answer(
        text=f"Assalomu alaykum {msg.from_user.first_name} 🤖\nBu Bot boshlovchi dasturchi tomonidan yaratilgan bo'lib! \nHato va kamchiliklar uchun uzur so'raymiz!")


@dp.message_handler(Text('🎧 All Music'))
async def all_music_handler(msg: types.Message):
    await msg.answer(text=f'Siz uchun ohirgi yangi musiqalar!')
    for i in main_data():
        await msg.answer_audio(i['track'], f"{i['artist']} - {i['title']}")


@dp.message_handler(Text('🎵 Tik-Tok Music'))
async def tik_tok_handler(msg: types.Message):
    text = 'Siz uchun top 10 Tik-Tok Musiqalar!\n\n'
    sana = 1
    for i in world_music():
        text += f"{str(sana)}. {i['artist']} - {i['title']}\n"
        sana += 1
    await msg.answer(text=text, reply_markup=world_track())


@dp.callback_query_handler(lambda x: x.data in [i['id'] for i in world_music()])
async def tik_tok_callback(callback: types.CallbackQuery):
    user_id = callback.data
    for i in world_music():
        if i['id'] == user_id:
            await callback.message.answer_audio(i['track'], f"{i['artist']} - {i['title']}")


@dp.message_handler(Text('🏆 Top Music'))
async def top_handler(msg: types.Message):
    text = 'Siz uchun top 10 Musiqalar!\n\n'
    sana = 1
    for i in top_music():
        text += f"{str(sana)}. {i['artist']} - {i['title']}\n"
        sana += 1
    await msg.answer(text=text, reply_markup=top_track())


@dp.callback_query_handler(lambda msg: msg.data in [i['id'] for i in top_music()])
async def welcome(callback: types.CallbackQuery):
    region_id = callback.data
    for i in top_music():
        if i['id'] == region_id:
            await callback.message.answer_audio(i['track'], f"{i['artist']} - {i['title']}")


@dp.message_handler(Text('🆕 New Music'))
async def new_music_handler(msg: types.Message):
    text = 'Siz uchun 10 yangi Musiqalar!\n\n'
    sana = 1
    for i in new_trek():
        text += f"{str(sana)}. {i['artist']} - {i['title']}\n"
        sana += 1
    await msg.answer(text=text, reply_markup=main_btn())


@dp.callback_query_handler(lambda x: x.data in [i['id'] for i in new_trek()])
async def new_callback_handler(callback: types.CallbackQuery):
    data_id = callback.data
    for i in new_trek():
        if data_id == i['id']:
            await callback.message.answer_audio(i['track'], f"{i['artist']} - {i['title']}")


@dp.callback_query_handler(lambda msg: msg.data == 'remove')
async def remove(callback: types.CallbackQuery):
    await callback.message.delete()


@dp.message_handler(Text('👨🏻‍💻 Admin'))
async def admin_handler(msg: types.Message):
    if msg.from_user.id == 5553781606:
        await msg.answer(text=f'{msg.from_user.first_name} admin sahifaga xush kelibsiz!', reply_markup=admin_page())
    else:
        await ReqState.fikrlar.set()
        await msg.answer(text='Talab va takliflaringizni yozib qoldiring!')


@dp.message_handler(Text('🔔 Reklama'))
async def rek_result(msg: types.Message):
    await ReklamaState.reklama.set()
    await msg.answer("Reklama Bo'limi!")


@dp.message_handler(Text('📊 Statistika'))
async def statistika(msg: types.Message):
    await msg.answer(text=f"Bot Obunachilari soni: {len(get_user())}")


@dp.message_handler(Text('🔙 Back'))
async def back_handler(msg: types.Message):
    await msg.answer(text='Bosh menyu!', reply_markup=start_btn())


@dp.message_handler(state=ReklamaState.reklama)
async def reklama_handler(msg: types.Message, state: FSMContext):
    await state.set_data({'reklama': msg.text})
    await msg.answer(text="Reklama jo'natish boshlandi!")
    data = await state.get_data()
    for i in get_user():
        if i[1] != str(5553781606):
            await bot.send_message(i[1], data['reklama'])
    await state.finish()


@dp.message_handler(state=ReqState.fikrlar)
async def comment_handler(msg: types.Message, state: FSMContext):
    await state.set_data({"comment": msg.text})
    await msg.answer(text='Sizning talab va takliflaringiz qabul qilindi!')
    data = await state.get_data()
    await bot.send_message(5553781606,
                           f"ID: {msg.from_user.id}\nFoydalanuvchi: {msg.from_user.username}\nFikrlar: {data['comment']}")
    await state.finish()


async def on_startup(dp):
    create_table()


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
