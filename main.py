from vk_api.longpoll import VkLongPoll, VkEventType
import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from datetime import datetime
import time
from datetime import datetime, timedelta
import pymysql.cursors

connection = pymysql.connect(host='localhost', user='root', password='password')
connection.close()

connect = pymysql.connect(host='localhost', user='root', password='password', db='my_db', charset='utf8mb4', cursorlass=pymysql.cursors.DictCursor)


token = "c9b64d3079680f4c7519fe69b1a516ea09c32daf1f0c755ab4eb93c3033bc2b50c5f44eac1a5559c0e8c7"
vk_session = vk_api.VkApi(token=token)

vk = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

def create_keyboard(responce):
    keyboard = VkKeyboard(one_time=False)
    if response == 'начать':
        keyboard.add_button('Подать заявку', VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button('Список модов для TVT игр', VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button('Обратиться к администрации', VkKeyboardColor.POSITIVE)


    elif responce == 'вернуться в главное меню':
        keyboard.add_button('Подать заявку', VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button('Список модов для TVT игр', VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button('Обратиться к администрации', VkKeyboardColor.POSITIVE)

    elif response == 'подать заявку':
        keyboard.add_button('Заявка на вступление в отряд', VkKeyboardColor.PRIMARY)
        keyboard.add_line()
        keyboard.add_button('Подача рапорта на специальность', VkKeyboardColor.PRIMARY)
        keyboard.add_line()
        keyboard.add_button('Подача рапорта на отпуск', VkKeyboardColor.PRIMARY)
        keyboard.add_line()
        keyboard.add_button('Вернуться в главное меню', VkKeyboardColor.NEGATIVE)

    elif response == 'закрыть':
        return keyboard.get_empty_keyboard()

    keyboard = keyboard.get_keyboard()
    return keyboard

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        print('Сообщение пришло в (МСК): ' + str(event.datetime + timedelta(hours=3)))
        print('Текст сообщения: ' + str(event.text))
        print(event.peer_id)
        response = event.text.lower()
        keyboard = create_keyboard(response)

        if event.from_chat or event.from_user:
                if response == 'вернуться в главное меню':
                    vk.messages.send(
                        peer_id=event.peer_id,
                        random_id=0,
                        message='Вы вернулись в главное меню!',
                        keyboard=keyboard,
                    )
                elif response == '/status' or response == '/статус':
                    today = datetime.strftime(datetime.now(), "%d%m%Y")
                    tomorrow = datetime.strftime(datetime.now() + timedelta(days=1), "%d%m%Y")
                    vk.messages.send(
                        peer_id=event.peer_id,
                        random_id=0,
                        message='Бот работает стабильно!' + '\n\nВсего сообщений в данном диалоге : ' +
                            str(vk.messages.search( peer_id=event.peer_id, date=tomorrow, count=1 )['count'] + 1),
                        keyboard=keyboard,
                    )
                elif response == 'подать заявку':
                    vk.messages.send(
                        peer_id=event.peer_id,
                        random_id=0,
                        message='Выберите необходимую форму ниже!',
                        keyboard=keyboard,
                    )
                    if response == 'заявка на вступление в отряд':
                        vk.messages.send(
                            peer_id=event.peer_id,
                            random_id=0,
                            message='Форма для завки: ',
                            keyboard=keyboard,
                        )