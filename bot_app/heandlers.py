from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import sqlite3

import os
import datetime

from settings import TOKEN
import keyboards as kb
from main import question_for_gpt

router = Router()
bot = Bot(TOKEN)


@router.message(F.text == '/start')
async def step1(message: Message):
    await message.answer('Старт работы бота', reply_markup=kb.start_conversation)


class Qwery(StatesGroup):
    qwery = State()


@router.callback_query(lambda callback_query: callback_query.data.startswith('start_conversation'))
async def qwery(message: Message, state: FSMContext):
    await state.set_state(Qwery.qwery)
    await bot.send_message(chat_id=message.from_user.id, text='Введите ваш запрос боту',
                           reply_markup=kb.start_conversation)


@router.message(Qwery.qwery)
async def neuro_answer(message: Message, state: FSMContext):
    await state.update_data(qwery=message.text)
    user_id = message.from_user.id

    conn = sqlite3.connect('client_context.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS user_context
                          (id INTEGER PRIMARY KEY AUTOINCREMENT, users_id INTEGER, context TEXT)''')
    cursor.fetchall()

    cursor.execute("SELECT users_id, context FROM user_context;")
    cursor.fetchall()

    cursor.execute(f"SELECT context FROM user_context "
                   f"WHERE users_id = {user_id};")
    str_context = cursor.fetchall()

    context = []
    for i in str_context:
        list_dicts = i[0].replace('[', '').replace(']', '').replace('},', '}//,').split('//,')
        dict_1, dict_2 = eval(list_dicts[0]), eval(list_dicts[1])
        context.append(dict_1)
        context.append(dict_2)

    context.append({'role': 'user', 'content': f'{message.text}'})
    answer = await question_for_gpt(context)
    context.append({'role': 'assistant', 'content': answer})

    object_data = (f'{user_id}', f'{context}')
    cursor.execute(f'''DELETE FROM user_context WHERE users_id = {user_id};''')
    cursor.execute('''INSERT INTO user_context (users_id, context) 
                            VALUES (?, ?)''', object_data)
    conn.commit()
    conn.close()

    await message.answer(text=f"{answer}", reply_markup=kb.start_conversation)
