from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='/start')]
],
                           resize_keyboard=True,
                           input_field_placeholder='Выберите пункт ниже')


start_conversation = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Задать вопрос', callback_data='start_conversation')],
])

stop_conversation = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Закончить диалог', callback_data='stop_conversation')],
])

