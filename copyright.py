
import os
import re
import sys
import time
import datetime
import random

from asyncio import sleep
from pyrogram import filters, Client, idle
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ChatMemberStatus, ChatType

from apscheduler.schedulers.background import BackgroundScheduler


API_ID = 6 
API_HASH = "Abcdefg1234"
BOT_TOKEN = ""
DEVS = [1696771874, 1128130156]

ALL_GROUPS = []
TOTAL_USERS = []
MEDIA_GROUPS = []
DISABLE_CHATS = []
GROUP_MEDIAS = {}

DELETE_MESSAGE = [
"1 Hour complete, I'm doing my work...",
"Its time to delete all medias!",
"No one can Copyright until I'm alive 😤",
"Hue hue, let's delete media...",
"I'm here to delete medias 🙋", 
"😮‍💨 Finally I delete medias",
"Great work done by me 🥲",
"All media cleared!",
"hue hue medias deleted by me 😮‍💨",
"medias....",
"it's hard to delete all medias 🙄",
]


RiZoeL = Client('DeleteAllMessage', api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

def add_user(user_id):
   if user_id not in TOTAL_USERS:
      TOTAL_USERS.append(user_id)

@RiZoeL.on_message(filters.command(["ping", "speed"]))
async def ping(_, e: Message):
   start = datetime.datetime.now()
   add_user(e.from_user.id)
   rep = await e.reply_text("**Pong !!**")
   end = datetime.datetime.now()
   ms = (end-start).microseconds / 1000
   await rep.edit_text(f"🤖 **PONG**: `{ms}`ᴍs")

@RiZoeL.on_message(filters.user(DEVS) & filters.command(["restart", "reboot"]))
async def restart_(_, e: Message):
   await e.reply("**Restarting.....**")
   try:
      await RiZoeL.stop()
   except Exception:
      pass
   args = [sys.executable, "copyright.py"]
   os.execl(sys.executable, *args)
   quit()

@RiZoeL.on_message(filters.user(DEVS) & filters.command(["stat", "stats"]))
async def status(_, message: Message):
   wait = await message.reply("Fetching.....")
   stats = "**Here is total stats of me!** \n\n"
   stats += f"Total Chats: `{len(ALL_GROUPS)}` \n"
   stats += f"Total users: `{len(TOTAL_USERS)}` \n"
   stats += f"Disabled chats: `{len(DISABLE_CHATS)}` \n"
   stats += f"Total Media active chats: `{len(MEDIA_GROUPS)}` \n\n"
   #stats += f"**© @RiZoeLX**"
   await wait.edit_text(stats)


   
@RiZoeL.on_message(filters.command(["delall"]))
async def enable_disable(Rizoel: RiZoeL, message: Message):
   chat = message.chat
   if chat.id == message.from_user.id:
      await message.reply("Use this command in group!")
      return
   txt = ' '.join(message.command[1:])
   if txt:
      member = await Rizoel.get_chat_member(chat.id, message.from_user.id)
      if re.search("on|yes|enable".lower(), txt.lower()):
         if member.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR] or member.user.id in DEVS:
            if chat.id in DISABLE_CHATS:
               await message.reply(f"Enabled DeleteAllMessage! for {chat.title}")
               DISABLE_CHATS.remove(chat.id)
               return
            await message.reply("Already enabled!")

      elif re.search("no|off|disable".lower(), txt.lower()):
         if member.status == ChatMemberStatus.OWNER or member.user.id in DEVS:
            if chat.id in DISABLE_CHATS:
               await message.reply("Already disabled!")
               return
            DISABLE_CHATS.append(chat.id)
            if chat.id in MEDIA_GROUPS:
               MEDIA_GROUPS.remove(chat.id)
            await message.reply(f"Disable DeleteAllMessage for {chat.title}!")
         else:
            await message.reply("Only chat Owner can disable DeleteAllMessage!")
            return 
      else:
         if member.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR] or member.user.id in DEVS:
            if chat.id in DISABLE_CHATS:
               await message.reply("DeleteAllMessage is disable for this chat! \n\ntype `/delall enable` to enable DeleteAllMessage")
            else:
               await message.reply("DeleteAllMessage is enable for this chat! \n\ntype `/delall disable` to disable DeleteAllMessage")
              
   else:
       if chat.id in DISABLE_CHATS:
          await message.reply("DeleteAllMessage is disable for this chat! \n\ntype `/delall enable` to enable DeleteAllMessage")
       else:
          await message.reply("DeleteAllMessage is enable for this chat! \n\ntype `/delall disable` to disable DeleteAllMessage")

@RiZoeL.on_message(filters.all & filters.group)
async def watcher(_, message: Message):
   chat = message.chat
   user_id = message.from_user.id
   if chat.type == ChatType.GROUP or chat.type == ChatType.SUPERGROUP:
      

      if chat.id not in ALL_GROUPS:
         ALL_GROUPS.append(chat.id)
      if chat.id in DISABLE_CHATS:
         return
      if chat.id not in MEDIA_GROUPS:
         if chat.id in DISABLE_CHATS:
            return
         MEDIA_GROUPS.append(chat.id)
      if (message.video or message.video_note or message.photo or message.audio or message.voice or message.animation or message.document or message.contact or message.location or message.web_page or message.sticker or message.text):
         check = GROUP_MEDIAS.get(chat.id)
         if check:
            GROUP_MEDIAS[chat.id].append(message.id)
            print(f"Chat: {chat.title}, message ID: {message.id}")
         else:
            GROUP_MEDIAS[chat.id] = [message.id]
            print(f"Chat: {chat.title}, message ID: {message.id}")

def AutoDelete():
    if len(MEDIA_GROUPS) == 0:
       return

    for i in MEDIA_GROUPS:
       if i in DISABLE_CHATS:
         return
       message_list = list(GROUP_MEDIAS.get(i))
       try:
          hue = RiZoeL.send_message(i, random.choice(DELETE_MESSAGE))
          RiZoeL.delete_messages(i, message_list, revoke=True)
          asyncio.sleep(1)
          hue.delete()
          GROUP_MEDIAS[i].delete()
       except Exception:
          pass
    MEDIA_GROUPS.remove(i)
    print("clean all media ✓")
    print("waiting for 1 hour")

scheduler = BackgroundScheduler()
scheduler.add_job(AutoDelete, "interval", seconds=43200)

scheduler.start()

def starter():
   print('starting bot...')
   RiZoeL.start()
   print('bot Started ✓')
   idle()

if __name__ == "__main__":
   starter()
