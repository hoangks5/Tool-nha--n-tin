from asyncio import events
from os import name
import re
from telethon import TelegramClient, events, hints, types
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
        res += int(i.split('/')[1])
    return res
def code_to_string(*args):
    strings = []
    count = 1
    for i in args[0]:
        row = '['+str(count)+'] <i>'+i.split('/')[0] +'</i> : <b>'+i.split('/')[1]+'</b> * '+str(ty_gia_vnd)+ ' = '+str("{:,}".format(int(i.split('/')[1])*ty_gia_vnd))
        strings.append(row)
        count +=1
    return '\n'.join(strings)
def vnd_code_to_string(*args):
    strings = []
    count = 1
    for i in args[0]:
        row = '['+str(count)+'] <i>'+i.split('/')[0] +'</i> : <b>'+str("{:,}".format(int(i.split('/')[1])))+'</b>'
        strings.append(row)
        count +=1
    return '\n'.join(strings)
def total_import_code(*args):
    total = args[0]
    res = 0
    for i in total:
        res += int(i.split('/')[1])
    return str(res)
def total_import_code_vnd(*args):
    total = args[0]
    res = 0
    for i in total:
        res += int(i.split('/')[1])
    res *= ty_gia_vnd
    return res


def xuat_file(import_code,vnd_import_code,ty_gia_vnd):
    time =[]
    time1 =[]
    value =[]
    value1 = []
    gia_tien = []
    for i in import_code:
        time.append(i.split('/')[0])
        value.append(i.split('/')[1])
        gia_tien.append(int(i.split('/')[1])*ty_gia_vnd)
    for j in vnd_import_code:
        time1.append(j.split('/')[0])
        value1.append(j.split('/')[1])
        
    can_tra = [total_import_code_vnd(import_code)]
    con_lai = [total_import_code_vnd(import_code)-vnd_total_import_code(vnd_import_code)]
    n_rows = max(len(time), len(time1))
    ty_gia = [ty_gia_vnd] * n_rows
    can_tra += [pd.NaT] * (n_rows - len(can_tra))
    con_lai += [pd.NaT] * (n_rows - len(con_lai))
    time += [pd.NaT] * (n_rows - len(time))
    gia_tien += [pd.NaT] * (n_rows - len(gia_tien))
    time1 += [pd.NaT] * (n_rows - len(time1))
    value += [pd.NaT] * (n_rows - len(value))
    value1 += [pd.NaT] * (n_rows - len(value1))
    print(con_lai)
    print(can_tra)
    print(gia_tien)
    
    df = pd.DataFrame({
        'Thời gian nhập mã': time,
        'Nhập mã': value,
        'Tỷ giá VND': ty_gia,
        'VND': gia_tien,
        'Thời gian nhận tiền': time1,
        'Nhận tiền': value1,
        'Cần trả': can_tra,
        'Còn lại': con_lai
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
                ty_le=int(number)
                
                
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
                ty_gia=int(number)
                
                
            if 'thiết lập tỷ giá vnd' in event.message.raw_text.lower():
                number = ''.join(re.findall(r'\d+\.\d+', event.message.raw_text))
                if number == '':
                    number = ''.join(re.findall(r'\d', event.message.raw_text))
                await client.send_message(GROUP_ID,'Thiết lập tỷ giá VND '+number)
                ty_gia_vnd=int(number)
                
            
            if event.message.raw_text[0] == '+':
                   
                    now = datetime.now()
                    current_time = now.strftime("%H:%M:%S")
                    number = ''.join(re.findall(r'\d+\.\d+', event.message.raw_text))
                    if number == '':
                        number = ''.join(re.findall(r'\d', event.message.raw_text))
                    import_code.append(current_time+'/'+number)
                    msg =   "<b>Nhập mã ("+str(len(import_code))+" mã)</b>\n"+code_to_string(import_code)+"\n\n<b>Nhận tiền ("+str(len(vnd_import_code))+" mã)</b>\n"+vnd_code_to_string(vnd_import_code)+"\n\nTổng nhập mã: <b>"+total_import_code(import_code)+"</b>\nPhí đổi: <b>"+str(ty_le)+"%</b>\nTỷ giá VND: <b>"+str(ty_gia_vnd)+"</b>\n\nCần trả: <b>"+str("{:,}".format(total_import_code_vnd(import_code)))+"</b> VND\n"+"Còn lại: <b>"+str("{:,}".format(total_import_code_vnd(import_code)-vnd_total_import_code(vnd_import_code)))+"</b> VND"
                    await client.send_message(GROUP_ID,message=msg,parse_mode='html')
            if event.message.raw_text[0] == '-':
    
                    now = datetime.now()
                    current_time = now.strftime("%H:%M:%S")
                    number = ''.join(re.findall(r'\d+\.\d+', event.message.raw_text))
                    if number == '':
                        number = ''.join(re.findall(r'\d', event.message.raw_text))
                    vnd_import_code.append(current_time+'/'+number)
                    msg =   "<b>Nhập mã ("+str(len(import_code))+" mã)</b>\n"+code_to_string(import_code)+"\n\n<b>Nhận tiền ("+str(len(vnd_import_code))+" mã)</b>\n"+vnd_code_to_string(vnd_import_code)+"\n\nTổng nhập mã: <b>"+total_import_code(import_code)+"</b>\nPhí đổi: <b>"+str(ty_le)+"%</b>\nTỷ giá VND: <b>"+str(ty_gia_vnd)+"</b>\n\nCần trả: <b>"+str("{:,}".format(total_import_code_vnd(import_code)))+"</b> VND\n"+"Còn lại: <b>"+str("{:,}".format(total_import_code_vnd(import_code)-vnd_total_import_code(vnd_import_code)))+"</b> VND"
                    await client.send_message(GROUP_ID,message=msg,parse_mode='html')
                    
            if 'sửa mã' in event.message.raw_text.lower().split('=')[0]:
                number = ''.join(re.findall(r'\d', event.message.raw_text.lower().split('=')[0]))
                value = ''.join(re.findall(r'\d+\.\d+', event.message.raw_text.lower().split('=')[1]))
                if value == '':
                    value = ''.join(re.findall(r'\d', event.message.raw_text.lower().split('=')[1]))
                await client.send_message(GROUP_ID,'Sửa thành công mã '+number+' = '+value)     
                import_code[int(number)-1] = import_code[int(number)-1].split('/')[0]+'/'+value
                msg =   "<b>Nhập mã ("+str(len(import_code))+" mã)</b>\n"+code_to_string(import_code)+"\n\n<b>Nhận tiền ("+str(len(vnd_import_code))+" mã)</b>\n"+vnd_code_to_string(vnd_import_code)+"\n\nTổng nhập mã: <b>"+total_import_code(import_code)+"</b>\nPhí đổi: <b>"+str(ty_le)+"%</b>\nTỷ giá VND: <b>"+str(ty_gia_vnd)+"</b>\n\nCần trả: <b>"+str("{:,}".format(total_import_code_vnd(import_code)))+"</b> VND\n"+"Còn lại: <b>"+str("{:,}".format(total_import_code_vnd(import_code)-vnd_total_import_code(vnd_import_code)))+"</b> VND"
                await client.send_message(GROUP_ID,message=msg,parse_mode='html')
                
            if 'xóa mã' in event.message.raw_text.lower():
                value = ''.join(re.findall(r'\d', event.message.raw_text))
                await client.send_message(GROUP_ID,'Xóa thành công mã '+value)     
                import_code.pop(int(value)-1)
                msg =   "<b>Nhập mã ("+str(len(import_code))+" mã)</b>\n"+code_to_string(import_code)+"\n\n<b>Nhận tiền ("+str(len(vnd_import_code))+" mã)</b>\n"+vnd_code_to_string(vnd_import_code)+"\n\nTổng nhập mã: <b>"+total_import_code(import_code)+"</b>\nPhí đổi: <b>"+str(ty_le)+"%</b>\nTỷ giá VND: <b>"+str(ty_gia_vnd)+"</b>\n\nCần trả: <b>"+str("{:,}".format(total_import_code_vnd(import_code)))+"</b> VND\n"+"Còn lại: <b>"+str("{:,}".format(total_import_code_vnd(import_code)-vnd_total_import_code(vnd_import_code)))+"</b> VND"
                await client.send_message(GROUP_ID,message=msg,parse_mode='html')
                
            if 'sửa vnd' in event.message.raw_text.lower().split('=')[0]:
                number = ''.join(re.findall(r'\d', event.message.raw_text.lower().split('=')[0]))
                value = ''.join(re.findall(r'\d+\.\d+', event.message.raw_text.lower().split('=')[1]))
                if value == '':
                    value = ''.join(re.findall(r'\d', event.message.raw_text.lower().split('=')[1]))
                await client.send_message(GROUP_ID,'Sửa thành công mã '+number+' = '+value)     
                vnd_import_code[int(number)-1] = import_code[int(number)-1].split('/')[0]+'/'+value
                msg =   "<b>Nhập mã ("+str(len(import_code))+" mã)</b>\n"+code_to_string(import_code)+"\n\n<b>Nhận tiền ("+str(len(vnd_import_code))+" mã)</b>\n"+vnd_code_to_string(vnd_import_code)+"\n\nTổng nhập mã: <b>"+total_import_code(import_code)+"</b>\nPhí đổi: <b>"+str(ty_le)+"%</b>\nTỷ giá VND: <b>"+str(ty_gia_vnd)+"</b>\n\nCần trả: <b>"+str("{:,}".format(total_import_code_vnd(import_code)))+"</b> VND\n"+"Còn lại: <b>"+str("{:,}".format(total_import_code_vnd(import_code)-vnd_total_import_code(vnd_import_code)))+"</b> VND"
                await client.send_message(GROUP_ID,message=msg,parse_mode='html')
                
            if 'xóa vnd' in event.message.raw_text.lower():
                value = ''.join(re.findall(r'\d', event.message.raw_text))
                await client.send_message(GROUP_ID,'Xóa thành công mã '+value)     
                vnd_import_code.pop(int(value)-1)
                msg =   "<b>Nhập mã ("+str(len(import_code))+" mã)</b>\n"+code_to_string(import_code)+"\n\n<b>Nhận tiền ("+str(len(vnd_import_code))+" mã)</b>\n"+vnd_code_to_string(vnd_import_code)+"\n\nTổng nhập mã: <b>"+total_import_code(import_code)+"</b>\nPhí đổi: <b>"+str(ty_le)+"%</b>\nTỷ giá VND: <b>"+str(ty_gia_vnd)+"</b>\n\nCần trả: <b>"+str("{:,}".format(total_import_code_vnd(import_code)))+"</b> VND\n"+"Còn lại: <b>"+str("{:,}".format(total_import_code_vnd(import_code)-vnd_total_import_code(vnd_import_code)))+"</b> VND"
                await client.send_message(GROUP_ID,message=msg,parse_mode='html')
            if event.message.raw_text.lower() == 'xuất file':
                await client.send_message(GROUP_ID,xuat_file(import_code, vnd_import_code,ty_gia_vnd)
                                              )
                await client.send_file(GROUP_ID, 'file.xlsx')
                os.remove('file.xlsx')
            if 'group_id' in event.message.raw_text.lower():
                value = ''.join(re.findall(r'\d', event.message.raw_text))
                GROUP_ID = int(value)
                await client.send_message(GROUP_ID,'Đổi thành công ID: '+str(GROUP_ID))
            
        else:
            pass
client.run_until_disconnected()
