from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import random
import Replies
from keyboards import *

api = ''
bot = Bot(token = api)
dp = Dispatcher(bot, storage = MemoryStorage())



# первая игра
'''YES OR NO'''
class Game1State(StatesGroup):
    waiting_for_question = State()

@dp.message_handler(text='Да или нет')
async def start_game(message):
    await message.answer(Replies.Game1_start, reply_markup= Game1Stop)
    await Game1State.waiting_for_question.set()


@dp.message_handler(state=Game1State.waiting_for_question)
async def answer_question(message, state):
    question = message.text.strip()

    if question == 'Остановить игру':
        await message.answer('Спасибо за игру!', reply_markup= start_menu)
        await state.finish()
        return

    if '?' not in question:
        await message.answer('Мне нужен вопрос с вопросительным знаком...')
        return

    await message.answer(random.choice(Replies.game_1_reps))

''''''



# вторая игра
'''GUESSGAME'''
class Game2State(StatesGroup):
    waiting_for_guess = State()

@dp.message_handler(text = 'Угадайка')
async def start_game(message: types.Message):
    await message.answer(text= Replies.Game2_start)
    await Game2State.waiting_for_guess.set()
    key_num = random.randint(1, 100)
    await dp.current_state(user=message.from_user.id).update_data(key_num=key_num, tries=8)

@dp.message_handler(state=Game2State.waiting_for_guess)
async def handle_guess(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    key_num = user_data.get('key_num')
    tries = user_data.get('tries')

    try:
        guess_num = int(message.text)
    except ValueError:
        await message.answer("Пожалуйста, введите число.")
        return

    if tries == 0:
        await message.answer(f'Почти получилось! Ваше число было {key_num}.', reply_markup=start_menu)
        await state.finish()
    elif guess_num > int(key_num):
        tries -= 1
        await message.answer(f'Слишком много! Попробуй еще. Осталось попыток: {tries}')
    elif guess_num < key_num:
        tries -= 1
        await message.answer(f'Слишком мало! Попробуй еще. Осталось попыток: {tries}')
    elif guess_num == key_num:
        await message.answer('Ты угадал! Поздравляю!', reply_markup= start_menu)
        await state.finish()  # Завершаем состояние игры
        return

    await state.update_data(tries=tries)
''''''




'''FIND WORD'''

class Game3State(StatesGroup):
    wait_for_q = State()

def digit_testing_find_game(a):
    return len(a) == 1

@dp.message_handler(text = 'Найди слово')
async def start_find_game(message: types.Message):
    word = random.choice(Replies.game_3_words)
    await dp.current_state().update_data(word=word)
    await message.answer(f'{Replies.Game3_start}{len(word)}\U000026A1',reply_markup= Game3Stop)
    await message.answer('Ваша буква: ')
    await Game3State.wait_for_q.set()


@dp.message_handler(state = Game3State.wait_for_q)
async def reply_find_game(message: types.Message, state: FSMContext):

    data = await state.get_data()
    digit = message.text.lower()
    word = data.get('word')

    if message.text == 'Остановить игру':
        await message.answer('Спасибо за игру!', reply_markup = game_keyb)
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
        await message.answer(f"Поздравляю! Вы угадали слово {word}!\U0001F44F", reply_markup= game_keyb )
        await state.finish()
    else:
        await message.answer(f"Текущий прогресс: {current_progress}")
        await message.answer('Введите следующую букву: ')

''''''




'''DEF COMMANDS'''
@dp.message_handler(text = 'Информация о боте\u2139')
async def about_message(message: types.Message):
    await message.answer(Replies.about)

@dp.message_handler(text = 'Игры\U0001F3AE')
async def about_message(message: types.Message):
    await message.answer('Выбери игру: ', reply_markup = game_keyb)
                                       # Завершаем состояние

@dp.message_handler(commands= ['start'])        # на какую команду реагировать
async def start_message(message):
    await message.answer(f'Привет, {message.from_user.username}! Поиграем?', reply_markup = start_menu)


@dp.message_handler(text = 'Назад')                          # реагирует на все
async def all_message(message):
    await message.answer('Выберите дальнейшее действие\U00002B07', reply_markup = start_menu)





if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
