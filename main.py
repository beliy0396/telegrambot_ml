from predict_model import model
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from states import States
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from aiogram.types import ReplyKeyboardMarkup
from aiogram.types import KeyboardButton
from aiogram import Bot, Dispatcher, types, executor

bot = Bot(token='5846028312:AAEipW2L_pJ7XgSM9Q7BPcTD7FWQXn87SWI')
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    inline_keyboard = types.InlineKeyboardMarkup()

    buttons = [
        types.InlineKeyboardButton(text="Узнать цену квартиры", callback_data="predict"),
        types.InlineKeyboardButton(text="Информация", callback_data="info"),
    ]
    inline_keyboard.add(*buttons)

    await message.answer("Привет👋")
    await message.answer("Я помогу тебе узнать примерную цену желаемой квартиры")
    await message.answer("Выбери действие:", reply_markup=inline_keyboard)




@dp.callback_query_handler(text="predict")
async def predict(call: types.CallbackQuery):
    await call.message.answer("Необходимо ввести данные о квартире:")
    await call.message.answer("Желаемая площадь(кв.м):")
    await States.get_area.set()

@dp.message_handler(state=States.get_area)
async def get_area(message: Message, state: FSMContext):
    area = message.text
    await state.update_data(
        {
            'area': area,
        }
    )
    await message.answer('Количество этажей в доме:')
    await States.next()

@dp.message_handler(state=States.get_floor_max)
async def get_floor_max(message: Message, state: FSMContext):
    floor_max = message.text
    await state.update_data(
        {
            'floor_max': floor_max,
        }
    )
    await message.answer('Этаж квартиры:')
    await States.next()

@dp.message_handler(state=States.get_floor)
async def get_floor(message: Message, state: FSMContext):
    floor = message.text
    await state.update_data(
        {
            'floor': floor,
        }
    )
    await message.answer('Количество комнат:')
    await States.next()

@dp.message_handler(state=States.get_rooms_count)
async def get_rooms_count(message: Message, state: FSMContext):
    rooms = message.text
    await state.update_data(
        {
            'rooms': rooms,
        }
    )

    buttons_type = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons_type.add(KeyboardButton('Лоджия'))
    buttons_type.add(KeyboardButton('Балкон'))


    await message.answer('Лоджия или балкон:', reply_markup=buttons_type)

    await States.next()


@dp.message_handler(Text(equals="Балкон"), state=States.get_extra_area_type_name)
async def get_extra_area_type_name(message: Message, state: FSMContext):
    type = message.text
    type = 0
    await state.update_data(
        {
            'type': type,
        }
    )
    buttons_water = ReplyKeyboardMarkup(resize_keyboard=True)
    buttons_water.add(KeyboardButton('Есть'))
    buttons_water.add(KeyboardButton('Нет'))

    await message.answer('Последний вопрос:', reply_markup=types.ReplyKeyboardRemove())
    await message.answer('Горячая вода?', reply_markup=buttons_water)
    await States.next()

@dp.message_handler(Text(equals="Лоджия"), state=States.get_extra_area_type_name)
async def get_extra_area_type_name(message: Message, state: FSMContext):
    type = message.text
    type = 1
    await state.update_data(
        {
            'type': type,
        }
    )
    buttons_water = ReplyKeyboardMarkup(resize_keyboard=True)
    buttons_water.add(KeyboardButton('Есть'))
    buttons_water.add(KeyboardButton('Нет'))

    await message.answer('Последний вопрос:', reply_markup=types.ReplyKeyboardRemove())
    await message.answer('Горячая вода?', reply_markup=buttons_water)
    await States.next()

@dp.message_handler(Text(equals="Есть"), state=States.get_hot_water)
async def get_hot_water(message: Message, state: FSMContext):
    hot_water = message.text
    hot_water = 1
    await state.update_data(
        {
            'hot_water': hot_water,
        }
    )
    data = await state.get_data()

    await state.finish()
    result = model.predict([[int(data['area']), int(data['floor_max']), int(data['floor']), int(data['rooms']), int(data['type']), int(data['hot_water'])]])

    if int(data['type']) == 1:
        type = 'Лоджия'
    else:
        type = 'Балкон'

    if int(data['hot_water']) == 1:
        water = 'Есть'
    else:
        water = 'Нет'

    await message.answer("Данные о квартире:", reply_markup=types.ReplyKeyboardRemove())
    await message.answer(f"Площадь: {int(data['area'])} кв.м\n"
                         f"Количество этажей в доме: {int(data['floor_max'])}\n"
                         f"Этаж квартиры: {int(data['floor'])}\n"
                         f"Количество комнат: {int(data['rooms'])}\n"
                         f"Тип: {type}\n"
                         f"Горячая вода: {water}\n")
    await bot.send_message(message.from_user.id, f"Примерная стоимость квартиры:\n{int(round(result[0][0], 0))} рублей💰💰💰")

@dp.message_handler(Text(equals="Нет"), state=States.get_hot_water)
async def get_hot_water(message: Message, state: FSMContext):
    hot_water = message.text
    hot_water = 0
    await state.update_data(
        {
            'hot_water': hot_water,
        }
    )
    data = await state.get_data()

    await state.finish()
    result = model.predict([[int(data['area']), int(data['floor_max']), int(data['floor']), int(data['rooms']), int(data['type']), int(data['hot_water'])]])

    if int(data['type']) == 1:
        type = 'Лоджия'
    else:
        type = 'Балкон'

    if int(data['hot_water']) == 1:
        water = 'Есть'
    else:
        water = 'Нет'

    await message.answer("Данные о квартире:", reply_markup=types.ReplyKeyboardRemove())
    await message.answer(f"Площадь: {int(data['area'])} кв.м\n"
                         f"Количество этажей в доме: {int(data['floor_max'])}\n"
                         f"Этаж квартиры: {int(data['floor'])}\n"
                         f"Количество комнат: {int(data['rooms'])}\n"
                         f"Тип: {type}\n"
                         f"Горячая вода: {water}\n")
    await bot.send_message(message.from_user.id, f"Примерная стоимость квартиры:\n{int(round(result[0][0], 0))} рублей💰💰💰")







executor.start_polling(dp, skip_updates=True)

