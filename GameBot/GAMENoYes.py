import random
import Replies
from keyboards import *
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

api = ''
bot = Bot(token = api)
dp = Dispatcher(bot, storage = MemoryStorage())

reps = ["Бесспорно", "Предрешено", "Никаких сомнений", "Определённо да","Можешь быть уверен в этом", "Мне кажется - да",
        "Вероятнее всего", "Хорошие перспективы", "Знаки говорят - да", "Да", "Пока неясно, попробуй снова",
        "Спроси позже", "Лучше не рассказывать", "Сейчас нельзя предсказать", "Сконцентрируйся и спроси опять",
        "Даже не думай", "Мой ответ - нет", "По моим данным - нет", "Перспективы не очень хорошие", "Весьма сомнительно"]

kb = ReplyKeyboardMarkup(
    keyboard= [
        [KeyboardButton(text= 'Остановить игру')]
    ], resize_keyboard= True
)

class Form(StatesGroup):
    waiting_for_question = State()

@dp.message_handler(commands=['start'])
async def start_game(message):
    await message.answer(Replies.yesno_hello, reply_markup= kb)
    await Form.waiting_for_question.set()


@dp.message_handler(state=Form.waiting_for_question)
async def answer_question(message, state):
    question = message.text.strip()

    if question == 'Остановить игру':
        await message.answer('Спасибо за игру!', reply_markup = start_menu)
        await state.finish()  # Завершаем состояние
        return

    if '?' not in question:
        await message.answer('Мне нужен вопрос с вопросительным знаком...')
        return

    await message.answer(random.choice(reps))


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)