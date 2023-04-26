import secret
import telebot
import requests
import random

from telebot import types

bot = telebot.TeleBot(token=secret.TOKEN)

name = "Капибара"
photo = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTWC4arfzIOz6WOMIzvmzOOkW6eu34E4Mw8Qw&usqp=CAU"


energy = 70
satiety = 10
happiness = 100

@bot.message_handler(commands=['start'])
def helloMessage(message):


    bot.send_message(message.from_user.id,'Введите имя своего питомца')
    bot.register_next_step_handler(message,set_name1)
def set_name1(message):
    global name
    name = message.text
    bot.register_next_step_handler(message,set_photo1)
    bot.send_message(message.from_user.id,"Скиньте фотографию вашего питомца (url) ")
def set_photo1(message):
    global photo
    photo = message.text

    global energy, satiety, happiness
    but1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    but1.add(types.KeyboardButton("/feed"))
    but1.add(types.KeyboardButton("/play"))
    but1.add(types.KeyboardButton("/sleep"))
    but1.add(types.KeyboardButton("/my_pet"))
    but1.add(types.KeyboardButton("/set_photo"))
    but1.add(types.KeyboardButton("/set_name"))
    bot.send_message(message.from_user.id,f"Привет, это твой {name}, тебе нужно кормить его, укладывать спать, играть, для поддержания характеристик.",reply_markup=but1)



@bot.message_handler(commands=['set_photo'])
def photo(message):
    bot.send_message(message.from_user.id,'Пришлите url фото')
    bot.register_next_step_handler(message,set_photo)

def set_photo(message):
    global photo
    photo = message.text
    print(photo)


@bot.message_handler(commands=['set_name'])
def name(message):
    bot.send_message(message.from_user.id,"Введите имя вашего питомца")
    bot.register_next_step_handler(message,set_name)

def set_name(message):
    global name
    name = message.text


def feed():
    global satiety,energy
    satiety += 20
    energy += 10

def play():
    global satiety,energy,happiness
    happiness += 10
    satiety -= 5
    energy -= 5

def sleep():
    global satiety,energy,happiness
    energy = 70
    satiety -= 10
    happiness -= 5


@bot.message_handler(commands=['feed'])
def feedHandler(message):
    feed()
    check(message)


@bot.message_handler(commands=['my_pet'])
def my(message):
    global happiness,satiety,energy
    bot.send_message(message.from_user.id,f"Характеристики вашего питомца: сытость - {satiety}, энергия - {energy}, усталость - {happiness}")
    bot.send_photo(message.from_user.id,photo,f'Ваш питомец - {name}')



@bot.message_handler(commands=['sleep'])
def sleepHandler(message):
    sleep()
    check(message)

@bot.message_handler(commands=['play'])
def playHandler(message):
    play()
    check(message)





@bot.message_handler(content_types=['text'])
def text_handler(message):
    pass




def check(message):
    global satiety,energy,happiness,name
    if satiety <= 0:
        bot.reply_to(message, f"Ваш {name} умер от голода!")

    elif satiety >= 150:
        bot.reply_to(message, f"Ваш {name} переел!")

    if energy <= 0:
        bot.reply_to(message, f"Ваш {name} умер от нехватки сил!")

    elif energy >= 200:
        bot.reply_to(message, f"Ваш {name} получил бешенство!")

    if happiness <= 0:
        bot.reply_to(message, f"Ваш {name} грустит, поиграй с ним!")
    elif happiness > 0:
        bot.reply_to(message, f"Ваш {name} счастлив!")


    print(f"S:{satiety},E:{energy},H:{happiness}")







bot.polling()
