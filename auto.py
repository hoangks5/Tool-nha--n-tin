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
from dotenv import load_dotenv, set_key
api_id = 8759328
api_hash = '1a270788cb618993f54f514f5a8c93c4'


admin = ['hoangkss5']
#GROUP_ID = -868013328

GROUP_ID = 'hoangkss5'


def set_up_config(ty_gia = None,ty_gia_vnd = None,ty_le = None):
    # Tải tệp .env
    load_dotenv()
    # Chỉnh sửa giá trị của một khóa
    if ty_gia != None:
        set_key('.env', 'ty_gia', ty_gia)
    if ty_le != None:
        set_key('.env', 'ty_le', ty_le)
    if ty_gia_vnd != None:
        set_key('.env', 'ty_gia_vnd', ty_gia_vnd)
def get_config(key):
    load_dotenv()
    # Lấy giá trị của một khóa
    api_key = os.getenv(key)
    return float(api_key)
    



client = TelegramClient('+84377820120', api_id, api_hash).start()
@client.on(events.NewMessage())
async def main(event):
        sender = await event.get_sender()
        if sender.username in admin:
            if 'đặt tỷ lệ' in event.message.raw_text.lower():
                number = ''.join(re.findall(r'\d+\.\d+', event.message.raw_text))
                if number == '':
                    number = ''.join(re.findall(r'\d', event.message.raw_text))
                await client.send_message(GROUP_ID,'Đặt tỷ lệ '+number+'%')
                set_up_config(ty_le=number)
                
                
            if event.message.raw_text == 'Bắt Đầu':
                await client.send_message(GROUP_ID,'Bắt Đầu Ghi Giao Dịch')
                data = []
            
            if 'thêm quản lý' in event.message.raw_text.lower():
                admin.append(event.message.raw_text.split('@')[1])
                await client.send_message(GROUP_ID,'Thêm quản lý @'+event.message.raw_text.split('@')[1])
            if 'xóa quản lý' in event.message.raw_text.lower():
                admin.append(event.message.raw_text.split('@')[1])
                await client.send_message(GROUP_ID,'Xoá quản lý @'+event.message.raw_text.split('@')[1])
            
            
            if 'thiết lập tỷ giá bằng' in event.message.raw_text.lower():
                number = ''.join(re.findall(r'\d+\.\d+', event.message.raw_text))
                if number == '':
                    number = ''.join(re.findall(r'\d', event.message.raw_text))
                await client.send_message(GROUP_ID,'Thiết lập tỷ giá bằng '+number+'%')
                set_up_config(ty_gia=number)
                
                
            if 'thiết lập tỷ giá vnd' in event.message.raw_text.lower():
                number = ''.join(re.findall(r'\d+\.\d+', event.message.raw_text))
                if number == '':
                    number = ''.join(re.findall(r'\d', event.message.raw_text))
                await client.send_message(GROUP_ID,'Thiết lập tỷ giá VND '+number+'%')
                set_up_config(ty_gia_vnd=number)
                
            
            if event.message.raw_text[0] == '+':
                try:
                    now = datetime.now()
                    current_time = now.strftime("%H:%M:%S")
                    number = ''.join(re.findall(r'\d+\.\d+', event.message.raw_text))
                    if number == '':
                        number = ''.join(re.findall(r'\d', event.message.raw_text))
                    data.append(current_time+'/'+number)
                    await client.send_message(GROUP_ID,'Nhập mã\n'+'\n'.join(data))
                except UnboundLocalError:
                    await client.send_message(GROUP_ID,'Bạn chưa bắt đầu giao dịch\nĐể bắt đầu giao dịch hãy chat Bắt Đầu')
                    
        else:
            pass
client.run_until_disconnected()
