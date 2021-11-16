import telebot
import config
from telebot import types
import json
import requests
import base64
from methods import *
import time
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)g

bot = telebot.TeleBot(config.token)

url = "https://api.imgbb.com/1/upload"

@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='Загрузить картино4ку', callback_data='upload'))
    bot.send_message(message.from_user.id, "Привет, я помогу тебе менеджить твои картиночки. \n\n"
                                           "Просто введи /upload или нажми на кнопку под этим сообщением!",
                     reply_markup=keyboard)
    return


@bot.message_handler(commands=['upload'])
def upload_request(message):
    upload(message.from_user.id, message)
    return


@bot.message_handler(commands=['get_tags'])
def tags_getter(message):
    try:
        test_connection()
    except Exception as ex:
        print(ex)
        session.rollback()
        time.sleep(3)
    try:
        instances = get_tags(message.from_user.id)
    except Exception as ex:
        print(ex)
        bot.send_message(message.from_user.id, 'Шо-то пошло не так... \n'
                                               'Шит хепенс🤷‍♀️')
        return

    if instances.__len__() < 1:
        bot.send_message(message.from_user.id, 'Соре, у вас нету ни одной картинки')
        return

    tag_list_unique = set()

    tag_list_text = 'Ваши теги картинок: \n\n'

    for image in instances:
        
        try:
            tag_list_unique.add(image.image_name.strip())
        except Exception as ex:
            print(ex)

    for tag in tag_list_unique:
        tag_list_text += f'{tag} \n'

    bot.send_message(message.from_user.id, tag_list_text)
    return


@bot.callback_query_handler(func=lambda call: True)
def answer_callback_query(call):

    if call.data == 'upload':
        upload(user_id=call.from_user.id, message=call.message)
        bot.answer_callback_query(call.id, text='', show_alert=False)
        return


def upload(user_id, message):
    bot.send_message(user_id, 'Отправь мне фото4ку')
    bot.register_next_step_handler(message, get_image)


def get_image(message):

    if message.content_type != 'photo':
        bot.send_message(message.from_user.id, 'Мне нужна фото4ка((((((...')
        bot.register_next_step_handler(message, get_image)
        return

    try:
        quantity = message.photo.__len__()
        raw = message.photo[quantity-1].file_id
    except Exception as ex:
        print(ex)
        bot.send_message(message.from_user.id, 'Шо-то пошло не так... \n'
                                               'Шит хепенс🤷‍♀️')
        return
    file_info = bot.get_file(raw)

    try:
        payload = {
            "key": config.api_access_key,
            "image": base64.b64encode(bot.download_file(file_info.file_path))
        }
    except Exception as ex:
        print(ex)
        return

    bot.send_message(message.from_user.id, 'Ждёмс, фото4ка заливается на сервер...')
    try:
        test_connection()
    except Exception as ex:
        print(ex)
        session.rollback()
        time.sleep(3)
    response = requests.post(url, payload)
    r = json.loads(response.text)

    try:
        image_id = create_image_instance(message.from_user.id, r['data']['url'], r['data']['thumb']['url'])
    except Exception as ex:
        print(ex)
        bot.send_message(message.from_user.id, 'Не удалось загрузить картиночку в бд(')
        return

    bot.send_message(message.from_user.id, 'Напиши название, или фразу по которых будешь искать ее')
    bot.register_next_step_handler(message, set_name, image_id)


def set_name(message, image_id):
    set_image_name(image_id, message.text)
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='Получить картино4ку', switch_inline_query_current_chat=' '))
    bot.send_message(message.from_user.id, 'Теперь можете попробовать ее найти', reply_markup=keyboard)


@bot.inline_handler(func=lambda query: len(query.query) > 0)
def inline_query(query):
    # offset = int(query.offset) if query.offset else 0
    try:
        test_connection()
    except Exception as ex:
        print(ex)
        session.rollback()
        time.sleep(3)
    try:
        images = get_image_by_name(query.from_user.id, query.query)
    except Exception as IE:
        print(IE)
        return
    if images is None:
        return
    images = set(images)
    ans = []

    for item in images:
        try:
            ans.append(types.InlineQueryResultPhoto(id=item.id, title=item.thumb_url,
                                                    photo_url=item.image_url, thumb_url=item.thumb_url))
        except Exception as ex:
            print(ex)
    # next_offset = offset+1 if ans.__len__() == 5 else offset
    # print(next_offset)
    bot.answer_inline_query(query.id, ans, cache_time=False)


if __name__ == '__main__':
    bot.polling(none_stop=True)
