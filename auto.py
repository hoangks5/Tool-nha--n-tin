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
import pandas as pd

admin = ['hoangkss5','RuanMengXiong']
GROUP_ID = -868013328

#GROUP_ID = 'hoangkss5'
import_code = []
vnd_import_code = []

ty_gia = 1000
ty_gia_vnd = 2000
ty_le = 0
def vnd_total_import_code(*args):
    total = args[0]
    res = 0
    for i in total:
        res += float(i.split('/')[1])
    return res
def code_to_string(*args):
    strings = []
    count = 1
    for i in args[0]:
        row = '['+str(count)+'] '+i.split('/')[0] +' : '+i.split('/')[1]+'*'+str(ty_gia_vnd)+ ' = '+str("{:,}".format(float(i.split('/')[1])*ty_gia_vnd))
        strings.append(row)
        count +=1
    return '\n'.join(strings)
def vnd_code_to_string(*args):
    strings = []
    count = 1
    for i in args[0]:
        row = '['+str(count)+'] '+i.split('/')[0] +' : '+str("{:,}".format(float(i.split('/')[1])))
        strings.append(row)
        count +=1
    return '\n'.join(strings)
def total_import_code(*args):
    total = args[0]
    res = 0
    for i in total:
        res += float(i.split('/')[1])
    return str(res)
def total_import_code_vnd(*args):
    total = args[0]
    res = 0
    for i in total:
        res += float(i.split('/')[1])
    res *= ty_gia_vnd
    return res


def xuat_file(import_code,vnd_import_code):
    time =[]
    time1 =[]
    value =[]
    value1 = []
    for i in import_code:
        time.append(i.split('/')[0])
        value.append(i.split('/')[1])
    for j in vnd_import_code:
        time1.append(j.split('/')[0])
        value1.append(j.split('/')[1])
        
    
    n_rows = max(len(time), len(time1))
    time += [pd.NaT] * (n_rows - len(time))
    time1 += [pd.NaT] * (n_rows - len(time1))
    value += [pd.NaT] * (n_rows - len(value))
    value1 += [pd.NaT] * (n_rows - len(value1))
    df = pd.DataFrame({
        'Thời gian nhập mã': time,
        'Nhập mã': value,
        'Thời gian nhận tiền': time1,
        'Nhận tiền': value1
    })
    
    df.to_excel("file.xlsx", index=True)
    return 'Xuất file thành công'


client = TelegramClient('+84377820120', api_id, api_hash).start()
@client.on(events.NewMessage())
async def main(event):
        global ty_gia, ty_gia_vnd, ty_le, import_code, vnd_import_code, admin, GROUP_ID
        sender = await event.get_sender()
        if sender.username in admin:
            if 'đặt tỷ lệ' in event.message.raw_text.lower():
                number = ''.join(re.findall(r'\d+\.\d+', event.message.raw_text))
                if number == '':
                    number = ''.join(re.findall(r'\d', event.message.raw_text))
                await client.send_message(GROUP_ID,'Đặt tỷ lệ '+number+'%')
                ty_le=float(number)
                
                
            if event.message.raw_text == 'Bắt Đầu':
                await client.send_message(GROUP_ID,'Bắt Đầu Ghi Giao Dịch Mới')
                import_code = []
                vnd_import_code = []
            
            
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
                await client.send_message(GROUP_ID,'Thiết lập tỷ giá bằng '+number)
                ty_gia=float(number)
                
                
            if 'thiết lập tỷ giá vnd' in event.message.raw_text.lower():
                number = ''.join(re.findall(r'\d+\.\d+', event.message.raw_text))
                if number == '':
                    number = ''.join(re.findall(r'\d', event.message.raw_text))
                await client.send_message(GROUP_ID,'Thiết lập tỷ giá VND '+number)
                ty_gia_vnd=float(number)
                
            
            if event.message.raw_text[0] == '+':
                   
                    now = datetime.now()
                    current_time = now.strftime("%H:%M:%S")
                    number = ''.join(re.findall(r'\d+\.\d+', event.message.raw_text))
                    if number == '':
                        number = ''.join(re.findall(r'\d', event.message.raw_text))
                    import_code.append(current_time+'/'+number)
                    await client.send_message(GROUP_ID,'Nhập mã ('+str(len(import_code))+' mã)\n'+code_to_string(import_code)+
                                              '\n\nNhận tiền ('+str(len(vnd_import_code))+' mã)\n'+vnd_code_to_string(vnd_import_code)+
                                              '\n\nTổng nhập mã: '+total_import_code(import_code)+
                                              '\nPhí đổi: '+str(ty_le)+'%\nTỷ giá VND: '+str(ty_gia_vnd)+
                                              '\n\nCần trả: '+str("{:,}".format(total_import_code_vnd(import_code)))+' VND\n'+
                                              'Còn lại: '+str("{:,}".format(total_import_code_vnd(import_code)-vnd_total_import_code(vnd_import_code)))+' VND'
                                              )
                    
            if event.message.raw_text[0] == '-':
    
                    now = datetime.now()
                    current_time = now.strftime("%H:%M:%S")
                    number = ''.join(re.findall(r'\d+\.\d+', event.message.raw_text))
                    if number == '':
                        number = ''.join(re.findall(r'\d', event.message.raw_text))
                    vnd_import_code.append(current_time+'/'+number)
                    await client.send_message(GROUP_ID,'Nhập mã ('+str(len(import_code))+' mã)\n'+code_to_string(import_code)+
                                              '\n\nNhận tiền ('+str(len(vnd_import_code))+' mã)\n'+vnd_code_to_string(vnd_import_code)+
                                              '\n\nTổng nhập mã: '+total_import_code(import_code)+
                                              '\nPhí đổi: '+str(ty_le)+'%\nTỷ giá VND: '+str(ty_gia_vnd)+
                                              '\n\nCần trả: '+str("{:,}".format(total_import_code_vnd(import_code)))+' VND\n'+
                                              'Còn lại: '+str("{:,}".format(total_import_code_vnd(import_code)-vnd_total_import_code(vnd_import_code)))+' VND'
                                              )
                    
            if 'sửa mã' in event.message.raw_text.lower().split('=')[0]:
                number = ''.join(re.findall(r'\d', event.message.raw_text.lower().split('=')[0]))
                value = ''.join(re.findall(r'\d+\.\d+', event.message.raw_text.lower().split('=')[1]))
                if value == '':
                    value = ''.join(re.findall(r'\d', event.message.raw_text.lower().split('=')[1]))
                await client.send_message(GROUP_ID,'Sửa thành công mã '+number+' = '+value)     
                import_code[int(number)-1] = import_code[int(number)-1].split('/')[0]+'/'+value
                await client.send_message(GROUP_ID,'Nhập mã ('+str(len(import_code))+' mã)\n'+code_to_string(import_code)+
                                              '\n\nNhận tiền ('+str(len(vnd_import_code))+' mã)\n'+vnd_code_to_string(vnd_import_code)+
                                              '\n\nTổng nhập mã: '+total_import_code(import_code)+
                                              '\nPhí đổi: '+str(ty_le)+'%\nTỷ giá VND: '+str(ty_gia_vnd)+
                                              '\n\nCần trả: '+str("{:,}".format(total_import_code_vnd(import_code)))+' VND\n'+
                                              'Còn lại: '+str("{:,}".format(total_import_code_vnd(import_code)-vnd_total_import_code(vnd_import_code)))+' VND'
                                              )
                
            if 'xóa mã' in event.message.raw_text.lower():
                value = ''.join(re.findall(r'\d', event.message.raw_text))
                await client.send_message(GROUP_ID,'Xóa thành công mã '+value)     
                import_code.pop(int(value)-1)
                await client.send_message(GROUP_ID,'Nhập mã ('+str(len(import_code))+' mã)\n'+code_to_string(import_code)+
                                              '\n\nNhận tiền ('+str(len(vnd_import_code))+' mã)\n'+vnd_code_to_string(vnd_import_code)+
                                              '\n\nTổng nhập mã: '+total_import_code(import_code)+
                                              '\nPhí đổi: '+str(ty_le)+'%\nTỷ giá VND: '+str(ty_gia_vnd)+
                                              '\n\nCần trả: '+str("{:,}".format(total_import_code_vnd(import_code)))+' VND\n'+
                                              'Còn lại: '+str("{:,}".format(total_import_code_vnd(import_code)-vnd_total_import_code(vnd_import_code)))+' VND'
                                              )
                
            if 'sửa vnd' in event.message.raw_text.lower().split('=')[0]:
                number = ''.join(re.findall(r'\d', event.message.raw_text.lower().split('=')[0]))
                value = ''.join(re.findall(r'\d+\.\d+', event.message.raw_text.lower().split('=')[1]))
                if value == '':
                    value = ''.join(re.findall(r'\d', event.message.raw_text.lower().split('=')[1]))
                await client.send_message(GROUP_ID,'Sửa thành công mã '+number+' = '+value)     
                vnd_import_code[int(number)-1] = import_code[int(number)-1].split('/')[0]+'/'+value
                await client.send_message(GROUP_ID,'Nhập mã ('+str(len(import_code))+' mã)\n'+code_to_string(import_code)+
                                              '\n\nNhận tiền ('+str(len(vnd_import_code))+' mã)\n'+vnd_code_to_string(vnd_import_code)+
                                              '\n\nTổng nhập mã: '+total_import_code(import_code)+
                                              '\nPhí đổi: '+str(ty_le)+'%\nTỷ giá VND: '+str(ty_gia_vnd)+
                                              '\n\nCần trả: '+str("{:,}".format(total_import_code_vnd(import_code)))+' VND\n'+
                                              'Còn lại: '+str("{:,}".format(total_import_code_vnd(import_code)-vnd_total_import_code(vnd_import_code)))+' VND'
                                              )
                
            if 'xóa vnd' in event.message.raw_text.lower():
                value = ''.join(re.findall(r'\d', event.message.raw_text))
                await client.send_message(GROUP_ID,'Xóa thành công mã '+value)     
                vnd_import_code.pop(int(value)-1)
                await client.send_message(GROUP_ID,'Nhập mã ('+str(len(import_code))+' mã)\n'+code_to_string(import_code)+
                                              '\n\nNhận tiền ('+str(len(vnd_import_code))+' mã)\n'+vnd_code_to_string(vnd_import_code)+
                                              '\n\nTổng nhập mã: '+total_import_code(import_code)+
                                              '\nPhí đổi: '+str(ty_le)+'%\nTỷ giá VND: '+str(ty_gia_vnd)+
                                              '\n\nCần trả: '+str("{:,}".format(total_import_code_vnd(import_code)))+' VND\n'+
                                              'Còn lại: '+str("{:,}".format(total_import_code_vnd(import_code)-vnd_total_import_code(vnd_import_code)))+' VND'
                                              )
            if event.message.raw_text.lower() == 'xuất file':
                await client.send_message(GROUP_ID,xuat_file(import_code, vnd_import_code)
                                              )
        else:
            pass
client.run_until_disconnected()
