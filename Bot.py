import requests
import telebot
from telebot import types

DATABASE = {
    'Долгопрудный': 'Dolgoprudny',
    'Москва': 'Moscow',
    'Санкт-Петербург': 'Saint Petersburg',
    'Новосибирск': 'Novosibirsk',
    'Ростов-на-Дону': 'Rostov-on-Don',
    'Екатеринбург': 'Yekaterinburg',
    'Казань': 'Kazan',
    'Краснодар': 'Krasnodar',
    'Ставрополь': 'Stavropol',
    'Владивосток': 'Vladivostok',
    'Красноярск': 'Krasnoyarsk',
    'Челябинск': 'Chelyabinsk',
    'Омск': 'Omsk',
    'Томск': 'Tomsk',
    'Калининград': 'Kaliningrad'
}

def weather(city):
    url = f'https://wttr.in/{city}'
    weather_parameters = {
        'format': 4,
        'M': ''
    }
    response = requests.get(url, params=weather_parameters)  # передаем параметры в http-запрос
    return(response.text)


commands_list = ['start']
bot = telebot.TeleBot('TOKEN')

@bot.message_handler(commands=['start'])
def start(message):
    photo = open('Hello.jpg', 'rb')
    bot.send_photo(message.chat.id, photo)
    description = 'Данный бот создан для показа погоды в выбранном городе.'
    answer = f'Привет, <b>{message.from_user.first_name}</b>! {description}'
    bot.send_message(message.chat.id, answer, parse_mode='html')

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    weather = types.KeyboardButton('Посмотреть погоду')
    site = types.KeyboardButton('Зайти на сайт')
    markup.add(weather, site)
    bot.send_message(message.chat.id, 'Что вы хотите сделать?', reply_markup=markup)

#@bot.message_handler(commands=['help'])
#def instructions(message):


@bot.message_handler(content_types=['text'])
def get_message(message):
    if message.text == 'Зайти на сайт':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Сайт', url='http://wttr.in'))
        bot.send_message(message.chat.id, 'Сайт, с которого взяты данные', parse_mode='html', reply_markup=markup)

    elif message.text == 'Посмотреть погоду':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        for cities in list(DATABASE.keys()):
            city = types.KeyboardButton(cities)
            markup.add(city)
        bot.send_message(message.chat.id,'Укажите город для прогноза погоды', reply_markup=markup)
    else:
        for city in list(DATABASE.keys()):
            if message.text == city:
                answer = weather(city)
                bot.send_message(message.chat.id, answer)


@bot.message_handler(content_types=['photo'])
def get_user_photo(message):
    bot.send_message(message.chat.id, 'Ничего себе, картинка! Но бот не знает что ответить <b>:(</b>', parse_mode='html')


@bot.message_handler(content_types=['sticker'])
def get_user_sticker(message):
    bot.send_message(message.chat.id, 'Ничего себе, стикер! Но бот не знает что ответить <b>:(</b>', parse_mode='html')


bot.polling(none_stop=True)



