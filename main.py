#cd /Users/a1/Documents/interneterabot
#git add .
#git commit -am "setup"
#git push heroku heroku:master


import asyncio
from aiogram import Bot, Dispatcher, executor, filters, types

import logging
import os
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils.executor import start_webhook
from aiogram.utils.markdown import text


TOKEN = os.environ['TOKEN']
import keyboards as kb

WEBHOOK_HOST = 'https://interneteratelebot.herokuapp.com'  # name your app
WEBHOOK_PATH = '/webhook/'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = os.environ.get('PORT')

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)


async def on_shutdown(dp):
    await bot.delete_webhook()


##Уведомления

@dp.callback_query_handler(func=lambda c: c.data == 'button1')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Нажата первая кнопка!')


@dp.callback_query_handler(func=lambda c: c.data and c.data.startswith('btn'))
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    code = callback_query.data[-1]
    if code.isdigit():
        code = int(code)
    if code == 2:
        await bot.answer_callback_query(callback_query.id, text='Нажата вторая кнопка')
    elif code == 5:
        await bot.answer_callback_query(
            callback_query.id,
            text='Нажата кнопка с номером 5.\nА этот текст может быть длиной до 200 символов 😉',
            show_alert=True)
    else:
        await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, f'Нажата инлайн кнопка! code={code}')

##

###keyboards
@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Привет!", reply_markup=kb.greet_kb)


@dp.message_handler(commands=['hi1'])
async def process_hi1_command(message: types.Message):
    await message.reply("Первое - изменяем размер клавиатуры",
                        reply_markup=kb.greet_kb1)


@dp.message_handler(commands=['hi2'])
async def process_hi2_command(message: types.Message):
    await message.reply("Второе - прячем клавиатуру после одного нажатия",
                        reply_markup=kb.greet_kb2)


@dp.message_handler(commands=['hi3'])
async def process_hi3_command(message: types.Message):
    await message.reply("Третье - добавляем больше кнопок",
                        reply_markup=kb.markup3)


@dp.message_handler(commands=['hi4'])
async def process_hi4_command(message: types.Message):
    await message.reply("Четвертое - расставляем кнопки в ряд",
                        reply_markup=kb.markup4)


@dp.message_handler(commands=['hi5'])
async def process_hi5_command(message: types.Message):
    await message.reply("Пятое - добавляем ряды кнопок",
                        reply_markup=kb.markup5)


@dp.message_handler(commands=['hi6'])
async def process_hi6_command(message: types.Message):
    await message.reply("Шестое - запрашиваем контакт и геолокацию\n"
                        "Эти две кнопки не зависят друг от друга",
                        reply_markup=kb.markup_request)


@dp.message_handler(commands=['hi7'])
async def process_hi7_command(message: types.Message):
    await message.reply("Седьмое - все методы вместе",
                        reply_markup=kb.markup_big)


@dp.message_handler(commands=['rm'])
async def process_rm_command(message: types.Message):
    await message.reply("Убираем шаблоны сообщений",
                        reply_markup=kb.ReplyKeyboardRemove())

@dp.message_handler(commands=['1'])
async def process_command_1(message: types.Message):
    await message.reply("Первая инлайн кнопка",
                        reply_markup=kb.inline_kb1)

@dp.message_handler(commands=['2'])
async def process_command_2(message: types.Message):
    await message.reply("Отправляю все возможные кнопки",
                        reply_markup=kb.inline_kb_full)
###keyboards

@dp.message_handler(text = 'one')
async def process_one_command(message: types.Message):
    await message.reply("Двое на кочелях") 
    await message("https://iframeab-pre2160.intickets.ru/node/10902005")

@dp.message_handler(commands=['cat'])
async def process_help_command(message: types.Message):
    # So... At first I want to send something like this:
    await message.reply("Do you want to see many pussies? Are you ready?")

    # And wait few seconds...
    await asyncio.sleep(1)

    # Good bots should send chat actions. Or not.
    await types.ChatActions.upload_photo()

    # Create media group
    media = types.MediaGroup()

    # You can also use URL's
    # For example: get random puss:
    media.attach_photo('http://lorempixel.com/400/200/cats/', 'Random cat.')

    # And you can also use file ID:
    # media.attach_photo('<file_id>', 'cat-cat-cat.')

    # Done! Send media group
    await message.reply_media_group(media=media)


# @dp.message_handler()
# async def echo_message(msg: types.Message):
#     await bot.send_message(msg.from_user.id, msg.text)

help_message = text(
    "Это урок по клавиатурам.",
    "Доступные команды:\n",
    "/start - приветствие",
    "\nШаблоны клавиатур:",
    "/hi1 - авто размер",
    "/hi2 - скрыть после нажатия",
    "/hi3 - больше кнопок",
    "/hi4 - кнопки в ряд",
    "/hi5 - больше рядов",
    "/hi6 - запрос локации и номера телефона",
    "/hi7 - все методы"
    "/rm - убрать шаблоны",
    "\nИнлайн клавиатуры:",
    "/1 - первая кнопка",
    "/2 - сразу много кнопок",
    sep="\n"
)


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply(help_message)



if __name__ == '__main__':
    start_webhook(dispatcher=dp, webhook_path=WEBHOOK_PATH,
                  on_startup=on_startup, on_shutdown=on_shutdown,
                  skip_updates=True, host=WEBAPP_HOST, port=WEBAPP_PORT)
