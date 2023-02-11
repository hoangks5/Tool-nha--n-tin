from asyncio import events
from os import name
import re
from telethon import TelegramClient, events, hints
from telethon.tl.functions.channels import JoinChannelRequest
import time
from telethon.tl.types import InputPeerChat
from telethon.tl.functions.messages import SendMessageRequest
import random
from telethon.tl.types import messages
from telethon.tl.functions.account import UpdateUsernameRequest
from telethon.tl.functions.photos import UploadProfilePhotoRequest
from telethon.tl.functions.account import UpdateProfileRequest
import os
from datetime import datetime

api_id = 8759328
api_hash = '1a270788cb618993f54f514f5a8c93c4'


admin = ['hoangkss5']
GROUP_ID = -868013328

def set_exchange_rate(number):
     with open('exchange_rate.log','w') as f:
          f.write(number)
          f.close()
def get_exchange_rate():
    with open('exchange_rate.log','r') as f:
        s = f.read()
        f.close()
    return int(s)

def set_total_value(number):
     with open('total_value.log','w') as f:
          f.write(number)
          f.close()
def get_total_value():
    with open('total_value.log','r') as f:
        s = f.read()
        f.close()
    return int(s)

client = TelegramClient('+84377820120', api_id, api_hash).start()
@client.on(events.NewMessage())
async def main(event):
        sender = await event.get_sender()
        #print(event.message.raw_text)
        if sender.username in admin:
            if '设置费率' in event.message.raw_text:
                await client.send_message(GROUP_ID,'Đặt tỷ lệ '+''.join(re.findall(r'\d', event.message.raw_text))+'%')
            if event.message.raw_text == '开始':
                await client.send_message(GROUP_ID,'Bắt Đầu')
            if '设置操作人' in event.message.raw_text:
                admin.append(event.message.raw_text.split('@')[1])
                await client.send_message(GROUP_ID,'Thêm quản lý @'+event.message.raw_text.split('@')[1])
            if '删除操作人' in event.message.raw_text:
                admin.append(event.message.raw_text.split('@')[1])
                await client.send_message(GROUP_ID,'Xoá quản lý @'+event.message.raw_text.split('@')[1])
            if '设置美元汇率' in event.message.raw_text:
                exchange_rate = int(''.join(re.findall(r'\d', event.message.raw_text)))
                await client.send_message(GROUP_ID,'Thiết lập tỷ giá bằng '+''.join(re.findall(r'\d', event.message.raw_text)))
            if '设置越南盾汇率' in event.message.raw_text:
                await client.send_message(GROUP_ID,'Thiết lập tỷ giá VND '+''.join(re.findall(r'\d', event.message.raw_text)))
                set_exchange_rate(''.join(re.findall(r'\d', event.message.raw_text)))
            if event.message.raw_text[0] == '+':

                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                code = ''.join(re.findall(r'\d', event.message.raw_text))
                total_value = get_total_value()+int(code)
                set_total_value(str(total_value))
                result = int(code)*get_exchange_rate()
                text = """Nhập mã(1 mã)\nThời gian: """+current_time+"""\n"""+code+""" * """+str(get_exchange_rate())+""" = """+str(result)+"""\n\nNhận tiền(0 mã)\n\n"""+"""Tổng nhập mã: """+str(total_value)+'\n'+'Phí đổi 0%\nVND: '+str(get_exchange_rate())+'\nCần trả: '+str(total_value*get_exchange_rate())+'\nCòn lại: '+str(total_value*get_exchange_rate())
                await client.send_message(GROUP_ID,text)
        else:
              pass
client.run_until_disconnected()
