from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from random import randint
import json
import time
import logging
from config import *

import asyncio
import aioschedule as schedule

started = False
wait = False
logging.basicConfig(format='%(name)s - %(levelname)s: %(message)s', level=logging.INFO)

app = Client(username, api_id, api_hash)

file_ids = []

@app.on_message()
async def on_bot_get_message(Client, message):
    global ids, file_ids, wait

    if message.from_user == None and message.chat.id == target and not wait:
        wait = True
        file_id = file_ids[randint(0, count)]
        await message.reply_animation(file_id)
        logging.info(f'Gif {file_id} sended')

    if message.text == "Update MessageId":
        ids = []

        for i in range(1, count+1):
            try:
                a = await app.send_animation(tech_group, f'static/{i}.gif')
            except FloodWait as e:     
                logging.info(f'Flood')
                await asyncio.sleep(e.x)
                a = await app.send_animation(tech_group, f'static/{i}.gif')
            await asyncio.sleep(8)
            ids.append(a.message_id)
            logging.info(f'Gif {i}')
            logging.debug(f'Message id {ids[-1]}')

        file_ids = []
        for i in await app.get_messages(tech_group, ids):
            file_ids.append(i.animation.file_id)
        logging.info('MessageId updated')
        logging.info(file_ids)

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
    schedule.every(600).seconds.do(true_wait)

    while True:
        await schedule.run_pending()
        await asyncio.sleep(2)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(scheduler())

started = True
logging.info('Bot started')
app.run()
