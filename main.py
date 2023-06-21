import asyncio
import random
import string

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot, Dispatcher
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from pyrogram import Client

from data import Data
from users import Users


def randomword():
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(10))


token = "5611863889:AAE-UpQbZBhmt7aosaLMydP1H7tm5RtKZ5k"
users = Users()
tokens_data = Data()
memory_storage = MemoryStorage()
bot = Bot(token=token, parse_mode="HTML")
dp = Dispatcher(storage=memory_storage)
scheduler = AsyncIOScheduler()
client_str = "BQAAAAAAjC-6N_3BV_JQ6Rr-NUC_MLKAjwoDRUgizo5bp1wjNeYSpUc5UoYMWCwedItuyDVLQ1UiDIaBC3CetUyp2sl1E8bL9ow31nKIHS4RGfwV_MI1ukOJaskCIy0IwzLHITxo_xx_mAaLc5vpqk9OVCrxRqM_CC70i3XXGvU8NR9s4ptx6pH2be1a0JYXvVzzyuKb8aoS2auZ8-aRl8-YHdlvca2p--UqbfyoVIGbi61_6eDdMRbjGvdwH2q67XIE7Th60uJ7Oq7yll3D1BH1v7OrOuUstPfKszYIBkg_n0eia-t89Ljg_r6fYjnwajyQXm_raCmx0b1HnqP2_COBkaNMOgAAAAAAACcPAA"
api_id = 6
api_hash = "eb06d4abfb49dc3eeb1aeb98ae0f581e"
client = Client("_", api_id=api_id, api_hash=api_hash, session_string=client_str, in_memory=True)


class States(StatesGroup):
    admin = State()
    user = State()
    no_user = State()
    add_channel_wait_message = State()
    add_channel_wait_admin = State()
    edit_channel = State()
    edit_channel_hours = State()


@dp.message(Command("start"))
async def start_command(message: Message, state: FSMContext):
    user = users.user(message.chat.id)
    if user.settings.admin:
        if user.settings.channel_id == 0:
            kb = InlineKeyboardBuilder()
            add_channel = InlineKeyboardButton(text="Добавить канал", callback_data="add_channel")
            add_user = InlineKeyboardButton(text="Добавить пользователя", callback_data="add_user")
            kb.row(add_channel)
            kb.row(add_user)
            await message.answer(
                text="Приветствую тебя, это админская панель\nТут можно добавть канал для именения ссылки, либо добавть пользователя",
                reply_markup=kb.as_markup())
        else:
            kb = InlineKeyboardBuilder()
            add_channel = InlineKeyboardButton(text="Редактировать канал", callback_data="edit_channel")
            add_user = InlineKeyboardButton(text="Добавить пользователя", callback_data="add_user")
            kb.row(add_channel)
            kb.row(add_user)
            await message.answer(
                text="Приветствую тебя, это админская панель\nТут можно редактировать канал для именения ссылки, либо добавть пользователя",
                reply_markup=kb.as_markup())
        await state.set_state(States.admin)
    elif user.settings.valid_user:
        if user.settings.channel_id == 0:
            kb = InlineKeyboardBuilder()
            add_channel = InlineKeyboardButton(text="Добавить канал", callback_data="add_channel")
            kb.row(add_channel)
            await message.answer(
                text="Приветствую тебя\nТут можно добавть канал для именения ссылки",
                reply_markup=kb.as_markup())
        else:
            kb = InlineKeyboardBuilder()
            add_channel = InlineKeyboardButton(text="Редактировать канал", callback_data="edit_channel")
            kb.row(add_channel)
            await message.answer(
                text="Приветствую тебя\nТут можно настроить изменение ссылки канала",
                reply_markup=kb.as_markup())
        await state.set_state(States.user)
    else:
        await message.answer(text="Приветствую тебя\nВведи свой код авторизации", )
        await state.set_state(States.no_user)
    user.save()


@dp.callback_query(Text("add_user"), States.admin)
async def confirm_command_tags(callback: CallbackQuery, state: FSMContext):
    user = users.user(callback.message.chat.id)
    if user.settings.admin:
        user_token = randomword()
        tokens_data.set_auth_token(user_token)
        await callback.message.answer(text=f"Токен для приглашения пользователя:{user_token}")


@dp.message(States.no_user)
async def confirm_command_tags(message: Message, state: FSMContext):
    user = users.user(message.chat.id)
    if tokens_data.has_auth_token(message.text):
        tokens_data.delete_auth_token(message.text)
        user.settings.valid_user = True
        await message.answer(text=f"Ваш аккаунт успешно активирован. Нажмите /start")
        user.save()
    else:
        await message.answer(text=f"Неверный токен. Введите корректный токен")


@dp.callback_query(Text("add_channel"), States.user)
@dp.callback_query(Text("add_channel"), States.admin)
async def confirm_command_tags(callback: CallbackQuery, state: FSMContext):
    user = users.user(callback.message.chat.id)
    if user.settings.valid_user or user.settings.admin:
        await callback.message.answer(text="Перешли сообщение из канала")
        await state.set_state(States.add_channel_wait_message)


@dp.message(States.add_channel_wait_message)
async def confirm_command_tags(message: Message, state: FSMContext):
    data = await state.get_data()
    try:
        if message.forward_from_chat.type == "channel":
            data["channel_id"] = message.forward_from_chat.id
        else:
            raise None
    except:
        await message.answer(text="Неккоректное сообщение. Попробуйте снова")
    else:
        kb = InlineKeyboardBuilder()
        ready = InlineKeyboardButton(text="Готово!", callback_data="ready")
        kb.row(ready)
        await message.answer(
            text="Добавьте @change_username_bot в администраторы канала и передайте ему право владения каналом",
            reply_markup=kb.as_markup())
        await state.set_state(States.add_channel_wait_admin)
        await state.set_data(data)


@dp.callback_query(Text("ready"), States.add_channel_wait_admin)
async def confirm_command_tags(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user = users.user(callback.message.chat.id)
    admins = await bot.get_chat_administrators(chat_id=data["channel_id"])
    for admin in admins:
        if admin.user.id == (await client.get_me()).id:
            try:
                await client.set_chat_username(data["channel_id"], randomword())
            except:
                await callback.message.answer(
                    text="Админ добавлен, но права владения не были переданны. Канал не добавлен")
            else:
                await callback.message.answer(
                    text="Канал успешно добавлен. Теперь можете его настроить, чтобы изменять ссылки /start")
                user.settings.channel_id = data["channel_id"]
                user.save()
                break
    else:
        await callback.message.answer(
            text="Не удалось добавить канал, попробуйте снова /start")


@dp.callback_query(Text("edit_channel"))
async def confirm_command_tags(callback: CallbackQuery, state: FSMContext):
    user = users.user(callback.message.chat.id)
    chat = await bot.get_chat(user.settings.channel_id)
    await chat.revoke_invite_link(chat.invite_link)
    kb = InlineKeyboardBuilder()
    set_channel = InlineKeyboardButton(text="Настроить", callback_data="set_channel")
    delete = InlineKeyboardButton(text="Удалить", callback_data="delete_channel")
    kb.row(set_channel)
    kb.row(delete)
    await callback.message.answer(
        text=f"Канал {chat.title}",
        reply_markup=kb.as_markup())
    await state.set_state(States.edit_channel_hours)


@dp.callback_query(Text("delete_channel"), States.edit_channel_hours)
async def confirm_command_tags(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        text="Канал успешно удален\nВернуться в начало /start")
    await state.set_state(States.edit_channel_hours)
    user = users.user(callback.message.chat.id)
    user.settings.channel_id = 0
    user.settings.hours = 0
    user.save()


@dp.callback_query(Text("set_channel"))
async def confirm_command_tags(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        text="Введите через какой промежуток времени изменять ссылку (в часах)")
    await state.set_state(States.edit_channel_hours)


@dp.message(States.edit_channel_hours)
async def confirm_command_tags(message: Message, state: FSMContext):
    if message.text.isdigit() and message.text != "0":
        user = users.user(message.chat.id)
        user.settings.hours = int(message.text)
        scheduler.add_job(change_link,
                          trigger='interval',
                          hours=user.settings.hours,
                          args=[message.chat.id],
                          id=str(message.chat.id)
                          )

        await message.answer(
            text=f"Канал успешно добавлен к работе. Ссылка будет меняться каждые {message.text} часов")
        user.save()
        await change_link(message.chat.id)
    else:
        await message.answer(
            text="Неккоректный формат. Попробуйте снова")


async def change_link(chat_id):
    user = users.user(chat_id)
    if user.settings.channel_id != 0 and user.settings.hours != 0:
        link = randomword()
        await client.set_chat_username(user.settings.channel_id, link)
        await bot.send_message(chat_id=chat_id, text=f"Новая ссылка: {link}")
    else:
        scheduler.remove_job(str(chat_id))


async def start():
    await client.start()
    scheduler.start()
    for user in users.get_all_users():
        if user.settings.hours != 0 and user.settings.channel_id != 0:
            scheduler.add_job(change_link,
                              trigger='interval',
                              hours=user.settings.hours,
                              args=[user.user_id],
                              id=str(user.user_id)
                              )
    print("bot started!")
    await dp.start_polling(bot, close_bot_session=False)


if __name__ == "__main__":
    asyncio.run(start())
