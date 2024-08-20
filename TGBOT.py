from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from config import *
from crud_functions import *
from Klaviatura import *

bot = Bot(token=api)
disp = Dispatcher(bot, storage=MemoryStorage())


class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = State()


@disp.message_handler(lambda message: message.text == "Регистрация", state="*")
async def start_registration(message: types.Message):
    await message.answer("Введите имя пользователя (только латинский алфавит):")
    await RegistrationState.username.set()


@disp.message_handler(state=RegistrationState.username)
async def process_username(message: types.Message, state: FSMContext):
    if not message.text.isascii():
        await message.answer("Пожалуйста, используйте только латинский алфавит.")
        return

    await state.update_data(username=message.text)
    await message.answer("Введите ваш email:")
    await RegistrationState.next()


@disp.message_handler(state=RegistrationState.email)
async def process_email(message: types.Message, state: FSMContext):
    await state.update_data(email=message.text)
    await message.answer("Введите ваш возраст:")
    await RegistrationState.next()


@disp.message_handler(lambda message: not message.text.isdigit(), state=RegistrationState.age)
async def process_age_invalid(message: types.Message):
    await message.answer("Возраст должен быть числом. Пожалуйста, введите корректный возраст.")


@disp.message_handler(lambda message: message.text.isdigit(), state=RegistrationState.age)
async def process_age(message: types.Message, state: FSMContext):
    await state.update_data(age=int(message.text))
    await message.answer("Введите ваш баланс:")
    await RegistrationState.next()


@disp.message_handler(lambda message: not message.text.replace('.', '', 1).isdigit(), state=RegistrationState.balance)
async def process_balance_invalid(message: types.Message):
    await message.answer("Баланс должен быть числом. Пожалуйста, введите корректный баланс.")


@disp.message_handler(lambda message: message.text.replace('.', '', 1).isdigit(), state=RegistrationState.balance)
async def process_balance(message: types.Message, state: FSMContext):
    await state.update_data(balance=float(message.text))
    user_data = await state.get_data()
    add_users(user_data['username'], user_data['email'], user_data['age'])
    if add_users is False:
        await message.answer("Такой пользователь уже существует!")
    else:
        await message.answer(
            f"Регистрация завершена! Ваши данные:\n"
            f"Имя пользователя: {user_data['username']}\n"
            f"Email: {user_data['email']}\n"
            f"Возраст: {user_data['age']}\n"
            f"Баланс: {user_data['balance']}"
        )
        await state.finish()



@disp.message_handler(text='Рассчитать')
async def main_menu(mess):
    await mess.answer(text='Выберите опцию:', reply_markup=INKboard_1)


@disp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer(text='10 х вес(кг) + 6,25 x рост(см) – 5 х возраст(г) + 5')
    await call.answer()


@disp.message_handler(text='Информация')
async def info(mess):
    await mess.answer('Тут будет информация о боте (но это не точно)')


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@disp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст')
    await UserState.age.set()
    await call.answer()


@disp.message_handler(state=UserState.age)
async def set_growth(mess, state):
    await state.update_data(age=mess.text)
    await mess.answer('Введите свой рост')
    await UserState.growth.set()


@disp.message_handler(state=UserState.growth)
async def set_weight(mess, state):
    await state.update_data(growth=mess.text)
    await mess.answer('Введите свой вес')
    await UserState.weight.set()


@disp.message_handler(state=UserState.weight)
async def send_calories(mess, state):
    await state.update_data(weight=mess.text)
    data = await state.get_data()
    calories = 10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) + 5
    await mess.answer(f'Ваши калории {calories}')
    await state.finish()


@disp.message_handler(commands=['start'])
async def consol_command(messe):
    await messe.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=KeyBoard)


@disp.message_handler(text="Купить")
async def get_buying_list(message):
    i = 1
    for num in all_products_1:
        with open(f"tablet_{i}.png", 'rb') as img:
            i += 1
            await message.answer_photo(img, num)
    await message.answer("Выберите продукт для покупки:", reply_markup=INKboard_2)


@disp.callback_query_handler(text="product_buying")
async def send_confirm_message(call):
    await call.message.answer("Вы успешно преобрели продукт!")
    await call.answer()


@disp.message_handler()
async def other_message(mess):
    await mess.answer('Введите команду /start, чтобы начать общение.')


if __name__ == "__main__":
    executor.start_polling(disp, skip_updates=True)
