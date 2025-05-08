import random
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

api = ''
bot = Bot(token = api)
dp = Dispatcher(bot, storage = MemoryStorage())

class Form(StatesGroup):
    waiting_for_guess = State()

@dp.message_handler(commands=['start'])
async def start_game(message: types.Message):
    key_num = random.randint(1, 100)  # Генерация числа от 1 до 100
    await message.answer(text='Угадайте число от 1 до 100. У вас 6 попыток.')
    await Form.waiting_for_guess.set()  # Устанавливаем состояние ожидания

    # cохраним сгенерированное число и количество попыток в контексте
    await dp.current_state(user=message.from_user.id).update_data(key_num=key_num, tries=6)

@dp.message_handler(state=Form.waiting_for_guess)
async def handle_guess(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    print(user_data, 'eeeeeeeeeeeeee')
    key_num = user_data.get('key_num')
    tries = user_data.get('tries')

    print(f"key_num: {key_num}, {type(key_num)}, tries: {tries}, {type(tries)}")

    try:
        guess_num = int(message.text)  # Пробуем преобразовать ввод в число
    except ValueError:
        await message.answer("Пожалуйста, введите число.")
        return

    if guess_num > int(key_num):
        tries -= 1
        await message.answer(f'Слишком много! Попробуй еще. Осталось попыток: {tries}')
    elif guess_num < key_num:
        tries -= 1
        await message.answer(f'Слишком мало! Попробуй еще. Осталось попыток: {tries}')
    else:
        await message.answer('Ты угадал! Поздравляю!')
        await state.finish()  # Завершаем состояние игры
        return

    if tries == 0:
        await message.answer(f'Попытки закончились! Ваше число было {key_num}.')
        await state.finish()  # Завершаем состояние игры

    # Обновляем количество оставшихся попыток в контексте
    await state.update_data(tries=tries)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
