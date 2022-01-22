from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from random import randint
import json
import time

import asyncio
import aioschedule as schedule

api_id = '' #Tg api id
api_hash = '' #Tg api hash
target = -0 #Tg group id to which to send gifs
tech_group = -0 #Tg group id that is needed for the fast work of the bot
count = 19
started = False
wait = False

app = Client("your_username", api_id, api_hash)

with open('ids.json', 'r') as fr:
    # Читаем из файла
    ids = json.load(fr)

file_ids = []

@app.on_message()
async def on_bot_get_message(Client, message):
    global ids, file_ids, wait

    if message.from_user == None and message.chat.id == target and not wait:
         wait = True
         await message.reply_animation(file_ids[randint(0, count)])

    if message.text == "Update MessageId":
         ids = []

         for i in range(1, count+1):
             try:
                 a = await app.send_animation(tech_group, f'static/{i}.gif')
                 await asyncio.sleep(8)
                 ids.append(a.message_id)
             except FloodWait as e:     
                 await asyncio.sleep(e.x)
                 a = await app.send_animation(tech_group, f'static/{i}.gif')
                 await asyncio.sleep(8)
                 ids.append(a.message_id)
         with open('ids.json', 'w') as fw:
             json.dump(ids, fw)

         file_ids = []
         for i in await app.get_messages(tech_group, ids):
             file_ids.append(i.animation.file_id)

async def get_file_id():
    global ids, file_ids, started
    if started:
        file_ids = []
        for i in await app.get_messages(tech_group, ids):
            print(i.animation.file_id)
            file_ids.append(i.animation.file_id)

async def true_wait():
    global wait
    wait = False

async def scheduler():
    schedule.every(7800).seconds.do(get_file_id)
    schedule.every(300).seconds.do(true_wait)

    while True:
        await schedule.run_pending()
        await asyncio.sleep(2)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(scheduler())

started = True
app.run()
