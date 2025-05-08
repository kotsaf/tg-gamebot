from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from keyboards import *
import random

api = ''
bot = Bot(token = api)
dp = Dispatcher(bot, storage = MemoryStorage())

# список слов
words = ['кот', 'дом', 'хит', 'сад', 'лев', 'пик', 'яма',
         'мама', 'сова', 'пума', 'воля', 'куры',
         'софия', 'сахар', 'мешок', 'веник',
         'солнце', 'анклав', 'лошадь']

# выбор слова
word = random.choice(words)

class Shape(StatesGroup):
    wait_for_q = State()

def digit_testing_find_game(a):
    return len(a) == 1

@dp.message_handler(text = 'Найди слово')
async def start_find_game(message: types.Message):
    word = random.choice(words)
    await dp.current_state().update_data(word=word)
    await message.answer(f'Угадай по буквам слово, которое я загадал! Букв в слове-{len(word)}', reply_markup= Game3Stop)
    await message.answer('Ваша буква: ')
    print(word)
    await Shape.wait_for_q.set()


@dp.message_handler(state = Shape.wait_for_q)
async def reply_find_game(message: types.Message, state: FSMContext):

    data = await state.get_data()
    digit = message.text.lower()
    word = data.get('word')

    if message.text == 'Остановить игру':
        await message.answer('Спасибо за игру!', reply_markup = start_menu)
        await state.finish()
        return


    if not digit_testing_find_game(digit):
        await message.answer('Вводите по одной букве!')

    user_data = await state.get_data()
    guessed_digits = user_data.get('guessed_digits', [])

    if digit not in guessed_digits:
        guessed_digits.append(digit)

    current_progress = ''.join([letter if letter in guessed_digits else '_' for letter in word])

    await state.update_data(guessed_digits=guessed_digits)


    if '_' not in current_progress:
        await message.answer(f"Поздравляем! Вы угадали слово {word}!\U0001F44F")
        await state.finish()
    else:
        await message.answer(f"Текущий прогресс: {current_progress}")
        await message.answer('Введите следующую букву: ', reply_markup= Game3Stop)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

