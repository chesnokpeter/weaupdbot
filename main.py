from pyowm import OWM
from pyowm.utils.config import get_default_config
import telebot
from telebot import *
from telebot import types
import requests
import datetime
# ---------- owm param ---------- 
config_dict = get_default_config()
config_dict["language"] = "RU"
config_dict['connection']['use_ssl'] = False
config_dict['connection']["verify_ssl_certs"] = False
owm = OWM('a99967bc9ee70d5b4bd387902982f400')
mgr = owm.weather_manager()
# ---------- other param ----------
bot = telebot.TeleBot("key")
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'}
# ---------- function param ----------
def getWeatherto (weather, times):
    global resultGetWeatherTo
    def futo(el):
        splitArray = el['dt_txt'].split(' ')
        time = splitArray[1]
        if time == times:
            return True
        else:
            return False
    resultGetWeatherTo = list(filter(futo, weather['list']))
def uuuuuu(m, n):
    global a, b, c, d, icon
    a = m[n]['weather'][0]['description'] #описание
    b = round(m[n]['main']['temp'], 1)    #градусы
    c = round(m[n]['wind']['speed'], 0)   #ветер
    d = m[n]['main']['humidity']          #влажность
    icon = m[n]['weather'][0]['icon']     #иконка

print("Go!")
# ---------- start ----------
if __name__=='__main__':
    while True:
        try:
            @bot.inline_handler(lambda query: len(query.query) > 0)
            def query_text(inline_query):
                # ----- param -----
                ntt = inline_query.query
                hour = str(datetime.datetime.now())
                hour = hour.split(' ')
                hour = hour[1].split(':')
                getTime = int(hour[0])
                try:
                    f = open('forecast_database.txt', 'a', encoding = 'utf-8')
                    f.write(f'{datetime.datetime.now()}    {inline_query.from_user.first_name} {inline_query.from_user.last_name} (@{inline_query.from_user.username})    {ntt}\n')
                    f.close()
                    # ----- param -----
                    observation = mgr.weather_at_place(ntt)
                    w = observation.weather
                    temp = w.temperature('celsius')["temp"]
                    wind = w.wind()['speed']
                    # ----- requests -----
                    response = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={ntt}&lang=ru&units=metric&appid=6623f2d9bf88a6f45c7f0b2c828aa328', headers=headers)
                    current = response.json()
                    icon = current["weather"][0]['icon']
                    fore = requests.get(f'http://api.openweathermap.org/data/2.5/forecast?q={ntt}&appid=6623f2d9bf88a6f45c7f0b2c828aa328&lang=ru&units=metric&cnt=40', headers=headers)
                    forecast = fore.json()

                    r = types.InlineQueryResultArticle(
                        '1', 
                        f"Сейчас {round(temp, 1)} °С",
                        types.InputTextMessageContent(f'⭐️ В городе {ntt}\n\n☁️ Сейчас {w.detailed_status}\n💡 Температура: {round(temp, 1)}° С\n🌬 Скорость вертра: {round(wind, 0)} м/с\n💧 Влажность: {w.humidity}%'),
                        description=f"☁️ {w.detailed_status}\n🌬 Скорость ветра: {round(wind, 0)} м/с",
                        thumb_url=f"http://openweathermap.org/img/wn/{icon}.png"
                    )
                    # ----- forecasts -----
                    if getTime <= 12:
                        getWeatherto(forecast, '12:00:00')
                        uuuuuu(resultGetWeatherTo, 0)
                        r2 = types.InlineQueryResultArticle(
                            '2', 
                            f"Сегодня днём {b} °С",
                            types.InputTextMessageContent(f'⭐️ В городе {ntt}\n\n☁️ Сегодня днём {a}\n💡 Температура: {b}° С\n🌬 Скорость ветра: {c} м/с\n💧 Влажность: {d}%'),
                            description=f"☁️ {a}\n🌬 Скорость ветра: {c} м/с",
                            thumb_url=f"https://openweathermap.org/img/wn/{icon}.png"
                        )
                        getWeatherto(forecast, '18:00:00')
                        uuuuuu(resultGetWeatherTo, 0)
                        r3 = types.InlineQueryResultArticle(
                            '3', 
                            f"Сегодня вечером {b} °С",
                            types.InputTextMessageContent(f'⭐️ В городе {ntt}\n\n☁️ Сегодня вечером {a}\n💡 Температура: {b}° С\n🌬 Скорость ветра: {c} м/с\n💧 Влажность: {d}%'),
                            description=f"☁️ {a}\n🌬 Скорость ветра: {c} м/с",
                            thumb_url=f"https://openweathermap.org/img/wn/{icon}.png"
                        )
                    # --
                    elif 12 < getTime <= 18:
                        getWeatherto(forecast, '18:00:00')         
                        uuuuuu(resultGetWeatherTo, 0)
                        r2 = types.InlineQueryResultArticle(
                            '2', 
                            f"Сегодня вечером {b} °С",
                            types.InputTextMessageContent(f'⭐️ В городе {ntt}\n\n☁️ Сегодня вечером {a}\n💡 Температура: {b}° С\n🌬 Скорость ветра: {c} м/с\n💧 Влажность: {d}%'),
                            description=f"☁️ {a}\n🌬 Скорость ветра: {c} м/с",
                            thumb_url=f"https://openweathermap.org/img/wn/{icon}.png"
                        )
                        getWeatherto(forecast, '00:00:00')
                        uuuuuu(resultGetWeatherTo, 0)
                        r3 = types.InlineQueryResultArticle(
                            '3', 
                            f"Сегодня ночью {b} °С",
                            types.InputTextMessageContent(f'⭐️ В городе {ntt}\n\n☁️ Сегодня ночью {a}\n💡 Температура: {b}° С\n🌬 Скорость ветра: {c} м/с\n💧 Влажность: {d}%'),
                            description=f"☁️ {a}\n🌬 Скорость ветра: {c} м/с",
                            thumb_url=f"https://openweathermap.org/img/wn/{icon}.png"
                        )
                    # --
                    elif 18 < getTime <= 24:                       
                        getWeatherto(forecast, '00:00:00')
                        uuuuuu(resultGetWeatherTo, 0)
                        r2 = types.InlineQueryResultArticle(
                            '2', 
                            f"Сегодня ночью {b} °С",
                            types.InputTextMessageContent(f'⭐️ В городе {ntt}\n\n☁️ Сегодня ночью {a}\n💡 Температура: {b}° С\n🌬 Скорость ветра: {c} м/с\n💧 Влажность: {d}%'),
                            description=f"☁️ {a}\n🌬 Скорость ветра: {c} м/с",
                            thumb_url=f"https://openweathermap.org/img/wn/{icon}.png"
                        )
                        r3 = types.InlineQueryResultArticle(
                            '3', 
                            "Место для вашей рекламы",
                            types.InputTextMessageContent('Место для вашей рекламы'),
                            description="Место для вашей рекламы",
                            thumb_url="https://cdn.discordapp.com/attachments/851529739843534889/1059187408287047821/logo.png"
                        )
                    # --
                    # ----- tomorrow -----
                    getWeatherto(forecast, '12:00:00')
                    uuuuuu(resultGetWeatherTo, 1)
                    r4 = types.InlineQueryResultArticle(
                        '4', 
                        f"Завтра днём {b} °С",
                        types.InputTextMessageContent(f'⭐️ В городе {ntt}\n\n☁️ Завтра днём {a}\n💡 Температура: {b}° С\n🌬 Скорость ветра: {c} м/с\n💧 Влажность: {d}%'),
                        description=f"☁️ {a}\n🌬 Скорость ветра: {c} м/с",
                        thumb_url=f"https://openweathermap.org/img/wn/{icon}.png"
                    )
                    # ----- after tomorrow -----
                    uuuuuu(resultGetWeatherTo, 2)
                    r5 = types.InlineQueryResultArticle(
                        '5', 
                        f"Послезавтра днём {b} °С",
                        types.InputTextMessageContent(f'⭐️ В городе {ntt}\n\n☁️ Послезавтра днём {a}\n💡 Температура: {b}° С\n🌬 Скорость ветра: {c} м/с\n💧 Влажность: {d}%'),
                        description=f"☁️ {a}\n🌬 Скорость ветра: {c} м/с",
                        thumb_url=f"https://openweathermap.org/img/wn/{icon}.png"
                    )

                    bot.answer_inline_query(inline_query.id, [r, r2, r3, r4, r5])
                except:
                    # ----- error -----
                    x = types.InlineQueryResultArticle(
                        '1', 
                        f"Город \"{ntt}\" не найден",
                        types.InputTextMessageContent('Город не найден'),
                    )
                    bot.answer_inline_query(inline_query.id, [x])
            # ---------- commands ----------
            @bot.message_handler(commands=['start'])
            def start_message(message):
                f = open('main_database.txt', 'a', encoding = 'utf-8')
                f.write(f'{datetime.datetime.now()}    {message.from_user.first_name} {message.from_user.last_name} (@{message.from_user.username})    /start\n')
                f.close()
                markup = types.InlineKeyboardMarkup()
                button1 = types.InlineKeyboardButton("Искать", switch_inline_query_current_chat="")
                markup.add(button1)
                bot.send_message(message.chat.id, text=f'👋 Привет {message.from_user.first_name}!\n\n🔍Чтобы найти ☁️погоду нажми на кнопку ниже👇 \n\n✅:  \"@weaupdbot белгород\"\n❌ :  \"@weaupdbotбелгород\"\n\n👤Также этого бота можно использовать в диалогах\n\nПо всем вопросам — @chesnokpeter', reply_markup=markup)

            @bot.message_handler(commands=['check'])
            def start_message(message):
                f = open('main_database.txt', 'a', encoding = 'utf-8')
                f.write(f'{datetime.datetime.now()}    {message.from_user.first_name} {message.from_user.last_name} (@{message.from_user.username})    /check\n')
                f.close()
                bot.send_message(message.chat.id, "Я работаю")

            @bot.message_handler(commands=['about'])
            def start_message(message):
                f = open('main_database.txt', 'a', encoding = 'utf-8')
                f.write(f'{datetime.datetime.now()}    {message.from_user.first_name} {message.from_user.last_name} (@{message.from_user.username})    /about\n')
                f.close()
                bot.send_message(message.chat.id, "Это бот с которым ты можешь отправлять 👥людям погоду ⛅️\n\nby_ @chesnokpeter")

            @bot.message_handler(commands=['file'])
            def start_message(message):
                f = open('main_database.txt', 'a', encoding = 'utf-8')
                f.write(f'{datetime.datetime.now()}    {message.from_user.first_name} {message.from_user.last_name} (@{message.from_user.username})    /file\n')
                f.close()
                bot.send_message(821785013, "main_database")
                f = open('main_database.txt', 'rb')
                bot.send_document(821785013, f)
                bot.send_message(821785013, "forecast_database")
                f = open('forecast_database.txt', 'rb')
                bot.send_document(821785013, f)

            @bot.message_handler(content_types=['text'])
            def send_echo(message):
                f = open('main_database.txt', 'a', encoding = 'utf-8')
                f.write(f'{datetime.datetime.now()}    {message.from_user.first_name} {message.from_user.last_name} (@{message.from_user.username})    {message.text}\n')
                f.close()

            # @bot.message_handler(content_types=['text'])
            # def send_echo(message):
            #     try:
            #         observation = mgr.weather_at_place(message.text)
            #         w = observation.weather
            #         temp = w.temperature('celsius')["temp"]
            #         wind = w.wind()['speed']
            #         answer = f"⭐️ В городе {message.text}\n\n☁️ Сейчас {w.detailed_status}\n💡 Температура: {round(temp, 1)}° С\n🌬 Скорость вертра: {round(wind, 0)} м/с\n💧 Влажность: {w.humidity}%"
            #     except:
            #         answer = "ошыбка"
            #     finally:
            #         bot.send_message(message.chat.id, answer)

            bot.polling(none_stop=True, interval=0)
        except Exception as e:
            print(datetime.datetime.now())
            print(e)
            print("ошибка")
            continue
