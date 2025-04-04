from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

game_keyb = ReplyKeyboardMarkup(
    keyboard= [
        [KeyboardButton(text = 'Угадайка'), KeyboardButton(text = 'Найди слово')],
        [KeyboardButton(text = 'Да или нет')],
        [KeyboardButton(text = 'Назад')]
    ], resize_keyboard= True
)

start_menu = ReplyKeyboardMarkup(
    keyboard= [
        [
            KeyboardButton(text= 'Информация о боте\u2139'),
            KeyboardButton(text= 'Игры\U0001F3AE')
        ]
    ], resize_keyboard= True
)


admin_panel = InlineKeyboardMarkup(
    inline_keyboard= [
        [InlineKeyboardButton('Пользователи', callback_data= 'users')],
        [InlineKeyboardButton('Статистика', callback_data= 'stat')],
        [
            InlineKeyboardButton('Блокировка', callback_data='block'),
            InlineKeyboardButton('Разблокировать', callback_data= 'unblock')
        ]
    ]
)

Game1Stop = ReplyKeyboardMarkup(
    keyboard= [
        [KeyboardButton(text= 'Остановить игру')]
    ], resize_keyboard= True
)

Game3Stop = ReplyKeyboardMarkup(
    keyboard= [
        [KeyboardButton('Остановить игру')]
    ], resize_keyboard= True
)


