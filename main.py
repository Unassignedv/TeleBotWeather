import requests
import telebot
from telebot import types

token = "5255*****88:******"
token_weather = "4d671b9************8"

bot = telebot.TeleBot(token)

city = "Moscow,RU"


@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.row("погода", "погода на неделю")
    bot.send_message(message.chat.id, 'Привет! Хочешь узнать погоду?', reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def answer(message):
    if message.text.lower() == "погода":
        res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                           params={'q': city, 'units': 'metric', 'lang': 'ru', 'APPID': token_weather})

        if res.status_code != 200:
            print("Ошибка подключении к weather api")
            exit(0)

        data = res.json()
        weather_message = f""" 
        Город: {city}\n
        Погодные условия: {data['weather'][0]['description']}\n
        Температура: {str(data['main']['temp'])}\n
        Скорость ветра: {str(data['wind']['speed'])}\n
        Видимость: {data['weather'][0]['description']}\n
        Минимальная температура: {str(data['main']['temp_min'])}\n
        Максимальная температура: {str(data['main']['temp_max'])}\n
        """
        bot.send_message(message.chat.id, weather_message)
    elif message.text.lower() == "погода на неделю":
        res = requests.get("http://api.openweathermap.org/data/2.5/forecast",
                           params={'q': city, 'units': 'metric', 'lang': 'ru', 'APPID': token_weather})

        if res.status_code != 200:
            print("Ошибка подключении к weather api")
            exit(0)

        data = res.json()
        for i in data['list']:
            bot.send_message(message.chat.id,
                             "Дата <" + i['dt_txt'] +

                             "> \r\nТемпература <" +
                             '{0:+3.0f}'.format(i['main']['temp']) +

                             "> \r\nПогодные условия <" +
                             i['weather'][0]['description'] +

                             "> \r\nСкорость ветра <" +
                             str(i['wind']['speed']) +
                             ">")
    else:
        bot.send_message(message.chat.id, "Команда не распознана")


bot.polling(none_stop=True, interval=0)
