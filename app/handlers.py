from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import app.keyboard as kb

router = Router()


class Register(StatesGroup):
    name = State()
    age = State()
    number = State()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer_photo(FSInputFile('photos/hi.jpg'), caption='Привет!', reply_markup=kb.main)

@router.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer(f'{message.from_user.first_name}, вам нужна помощь?')
    await message.answer(f'Ваш ID: {message.from_user.id}')

@router.message(F.text == "Каталог")
async def catalog(message: Message):
    await message.answer('Выберите категорию товара', reply_markup=kb.catalog)


@router.callback_query(F.data == 't-shirt')
async def t_shirt(callback: CallbackQuery):
    await callback.answer("Вы выбрали категорию", show_alert=True)
    await callback.message.answer("Вы выбрали категорию футболок")




@router.message(Command('register'))
async def register(message: Message, state: FSMContext):
    await state.set_state(Register.name)
    await message.answer('Введите ваше имя')

@router.message(Register.name)
async def register_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Register.age)
    await message.answer("Введите ваш возраст")

@router.message(Register.age)
async def register_age(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await state.set_state(Register.number)
    await message.answer("Отправьте ваш номер телефона", reply_markup=kb.get_number)

@router.message(Register.number, F.contact)
async def register_number(message: Message, state: FSMContext):
    await state.update_data(number=message.contact.phone_number)
    data = await state.get_data()
    await message.answer(f'Ваше имя: {data["name"]}\nВаш возраст: {data["age"]}\nНомер: {data["number"]}',
                         reply_markup=kb.main)
    await state.clear()



@router.message()
async def echo(message: Message):
    await message.answer("Неизвестная команда")