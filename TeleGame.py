import threading
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command

from Core import *

logging.basicConfig(level=logging.INFO)

bot = Bot("")

dp = Dispatcher()

init(bot)

@dp.message(Command("start"))
async def cmd_start(message: types.Message):

    await message.answer("✋Вітаю вас у моєму боті\n⚓Я б хотів презентувати вам свою гру, морський бій.\n\nЦе мультиплеєрна гра, тому потрібно як мінімум двоє гравців вони можуть бути на різних девайсах.\nЦе бета версія тому можуть бути баги можите повітомити про них мені👉@multy_prizm")
    await message.answer("❓Як грати:\n\nЩоб почати гру напишіть /go\n🚀Щоб зробити постріл напишіть у чат букву і цифту потрібної клітинки\n📡Не забувайте використовувати радіо зв'язок /radio щоб бути вкурсі ситуації на фронті\n\n🖥Рекомендується грати з комп'ютери чи ноудбука")

    if not message.chat.id in Conections:
        Conections.append(message.chat.id)

@dp.message(Command("info"))
async def cmd_start(message: types.Message):

    await message.answer("❓Як грати:\n\nЩоб почати гру напишіть /go\n🚀Щоб зробити постріл напишіть у чат букву і цифту потрібної клітинки\n📡Не забувайте використовувати радіо зв'язок /radio щоб бути вкурсі ситуації на фронті\n\n🖥Гра розрахованя тілька на комп'ютери чи ноудбуки")

    if not message.chat.id in Conections:
        Conections.append(message.chat.id)

@dp.message(Command("go"))
async def cmd_start(message: types.Message):

    if not message.chat.id in IndexDict and not message.from_user.first_name in LineDict:

        LineDict[message.from_user.first_name] = message.chat.id

        await message.answer("⚓Твій флот вийшов з порту в пошуках неприємностей\n📡Використовуй /radio щоб дізнатися чи все добре")
    else:
        await message.answer("🛑Ти вже у грі")
    
    if not message.chat.id in Conections:
        Conections.append(message.chat.id)

@dp.message(Command("exit"))
async def cmd_start(message: types.Message):

    if message.chat.id in IndexDict and not message.from_user.first_name in LineDict:

        IndexDict[message.chat.id].exit(message.chat.id)

        await message.answer(IndexDict[message.chat.id].out(message.chat.id))
    else:
        await message.answer("🛑Ти не у грі\n/go - щоб почати гру")
    
    if not message.chat.id in Conections:
        Conections.append(message.chat.id)

@dp.message(Command("Code3478632784798356341783246389"))
async def cmd_start(message: types.Message):

    text = "‼️Наданий момент бота вимкнено‼️\n\nПодяка від @multy_prizm за, що прийняли участь у бета тесті."

    for i in Conections:
        await bot.send_message(i, text)


@dp.message(Command("radio"))
async def cmd_start(message: types.Message):

    if message.chat.id in IndexDict:
        text = IndexDict[message.chat.id].out(message.chat.id)

        if text != "":
            text = text.split("%")

        if text != "" and type(text) == type([]):
            for i in text:
                await message.answer(i)
        elif text != "":
            await message.answer(text)
        else:
            await message.answer("📡Немає нової інформації")

    elif message.from_user.first_name in LineDict:
        await message.answer("📡Все добре, покищо")

    else:
        await message.answer("🛑Ти не у грі\n/go - щоб почати гру")
    
    for i in Conections:

        if i in IndexDict:
            text = IndexDict[i].out(i)

            if text != "":
                text = text.split("%")

            if text != "" and type(text) == type([]):
                for s in text:
                    await bot.send_message(i, s)
            elif text != "":
                await bot.send_message(i, text)
    
    if not message.chat.id in Conections:
        Conections.append(message.chat.id)

@dp.message()
async def echo(message: types.Message):
    
    text = message.text.lower()

    if message.chat.id in IndexDict:
        if not IndexDict[message.chat.id].end:
            if IndexDict[message.chat.id].check_status(message.chat.id):
                if IndexDict[message.chat.id].check_status(message.chat.id):
                    if len(text) <= 3 and len(text) > 1:
                        if text[0] in "abcdefghij":

                            if text in "0" and text in "1":

                                IndexDict[message.chat.id].put_mess(message.chat.id, text)
                                await message.answer("🚀Вогонь "+ message.text)
                                await message.answer("🚨Увага противник готує відповідь")
                            
                            if text[1] in "123456789":
                                IndexDict[message.chat.id].put_mess(message.chat.id, text)
                                await message.answer("🚀Вогонь "+ message.text)
                                await message.answer("🚨Увага противник готує відповідь")

                        else:
                            await message.answer("🛑Некоректрі кординати")
                    else:
                        await message.answer("🛑Некоректрі кординати")
            else:
                await message.answer("🛑Зараз черга противника")
        else:
            await message.answer(IndexDict[message.chat.id].out(message.chat.id))
    else:
        await message.answer("🛑Ти не у грі\n/go - щоб почати гру")
    
    if not message.chat.id in Conections:
        Conections.append(message.chat.id)

async def main():
    await dp.start_polling(bot)

def runBot():
    asyncio.run(main())


threading.Thread(target=runBot).start()
threading.Thread(target=foo).start()
threading.Thread(target=selection).start()
threading.Thread(target=Processing).run()