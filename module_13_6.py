from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio


api = ''
bot = Bot(token = api)
dp = Dispatcher(bot, storage= MemoryStorage())

kb2 = ReplyKeyboardMarkup(resize_keyboard = True)
btn = KeyboardButton(text = 'Рассчитать')
btn1 = KeyboardButton(text = 'Информация')
kb2.insert(btn)
kb2.insert(btn1)

kb = InlineKeyboardMarkup()
button1 = InlineKeyboardButton(text = 'Рассчитать норму калорий', callback_data= 'calories')
button2 = InlineKeyboardButton(text = 'Формулы расчёта', callback_data='formulas')
kb.insert(button1)
kb.insert(button2)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(text= 'Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию', reply_markup=kb)

@dp.callback_query_handler(text= 'formulas')
async def get_formulas(call):
    await call.message.answer('Для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5;\n'
    'Для женщин: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161.')
    await call.answer()

@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup = kb2)

@dp.callback_query_handler(text= 'calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await call.answer()
    await UserState.age.set()

@dp.message_handler(state= UserState.age)
async def set_growth(message, state):
    await state.update_data(age = message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()

@dp.message_handler(state= UserState.growth)
async def set_weight(message, state):
    await state.update_data(weight = message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()

@dp.message_handler(state= UserState.weight)
async def send_calories(message, state):
    await state.update_data(growth = message.text)
    data = await state.get_data()
    cal = 10 * int(data["weight"]) + 6.25 * int(data["growth"]) - 5 * int(data["age"]) + 5
    await message.answer(f'Ваша норма калорий {cal}')
    await state.finish()

@dp.message_handler()
async def all_massages(message):
    print('Введите команду /start, чтобы начать общение.')
    await message.answer('Введите команду /start, чтобы начать общение.')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)