from bot_long_poll.dcs import Message, Payload, Update, UpdateObject
from vk_api.dcs import User

user1 = User(first_name="Максим", last_name="Милованов")
user2 = User(first_name="Леонид", last_name="Якубович")

about_response_message = {'user_id': 83106437,
                          'text': 'Поле Чудес - советская и российская телеигра, выходящая каждую пятницу в 19:45 и являющаяся\
                           частичным аналогом американской телевизионной программы «Колесо Фортуны»',
                          'response': {'response': 7136}}
start_command_response_message = {'user_id': 83106437,
                                  'text': 'Добро пожаловать в игру Поле Чудес!!\
                                           Вы можете играть в игру один или пригласить друзей.\
                                           Максимальное количество игроков 3.',
                                  'response': {'response': 7157}}
game_request_response_message = {'user_id': 83106437,
                                 'text': 'Максим Милованов отправил(а) заявку на игру в Поле Чудес.\
                                 \nКоличество зарегистрированых игроков - 1\
                                 \n Игроки: \n1. Максим Милованов',
                                 'response': {'response': 7159}}

start_game_response_message = {'user_id': 83106437,
                               'text': 'Игра началась!! Внимание вопрос.\
                               \nТема вопроса: Профессии\
                               \nВопрос: Специалист по отделке зданий или помещений.\
                               \nСлово из 5 букв\
                               \nСлово: *****\
                               \n Чтобы назвать все слово сразу отправьте сообщение',
                               'response': {'response': 7183}}


guess_letter_correct_response_message = {'user_id': 83106437,
                                         'text': 'Буква м в слове присутствует.\
                                         \nЗа правильный ответ начислено баллов: 14\
                                         \nВсего баллов: 14\
                                         \nСлово: ****р\
                                         \nВаш следующий ход.',
                                         'response': {'response': 7185}}
guess_letter_incorrect_response_message = {'user_id': 83106437,
                                           'text': 'Неверный ответ. Ход переходит к игроку: Леонид Якубович.',
                                           'response': {'response': 7187}}

guess_word_correct_response_message = {'user_id': 83106437,
                                       'text': 'Победу одержал(а): Максим Милованов\n Ответ: маляр',
                                       'response': {'response': 7173}}
guess_word_incorrect_response_message = {'user_id': 83106437,
                                         'text': 'Вы неверно назвали слово. Игра окончена.',
                                         'response': {'response': 7179}}


COMMANDS_USER1 = {
    "start": Update(
        type='message_new',
        object=UpdateObject(message=Message(
            from_id=83106437,
            text='Начать', id=7095,
            payload=Payload(command='start', letter=None)))),
    "game_request": Update(
        type='message_new',
        object=UpdateObject(message=Message(
            from_id=83106437,
            text='Отправить заявку на игру',
            id=7097,
            payload=Payload(command='game_request', letter=None)))),
    "about": Update(
        type='message_new',
        object=UpdateObject(message=Message(
            from_id=83106437,
            text='Об игре',
            id=7103,
            payload=Payload(command='about', letter=None)))),
    "start_game": Update(
        type='message_new',
        object=UpdateObject(message=Message(
            from_id=83106437,
            text='Играть',
            id=7107,
            payload=Payload(command='start_game', letter=None)))),
    "guess_letter_correct": Update(
        type='message_new',
        object=UpdateObject(message=Message(
            from_id=83106437,
            text='м',
            id=7109,
            payload=Payload(command='guess_letter', letter='Рї')))),
    "guess_letter_incorrect": Update(
        type='message_new',
        object=UpdateObject(message=Message(
            from_id=83106437,
            text='ъ',
            id=7109,
            payload=Payload(command='guess_letter', letter='Рї')))),
    "quite": Update(
        type='message_new',
        object=UpdateObject(message=Message(
            from_id=83106437,
            text='Выйти из игры',
            id=7111,
            payload=Payload(command='quite', letter=None)))),
    "cancel_game_request": Update(
        type='message_new',
        object=UpdateObject(message=Message(
            from_id=83106437,
            text='Отменить заявку',
            id=7115,
            payload=Payload(command='cancel_game_request', letter=None)))),
    "начать": Update(
        type='message_new',
        object=UpdateObject(message=Message(
            from_id=83106437,
            text='начать',
            id=7117,
            payload=None))),
    "guess_word_correct": Update(
        type='message_new',
        object=UpdateObject(message=Message(
            from_id=83106437,
            text='маляр',
            id=7172, payload=None))),
    "guess_word_incorrect": Update(
        type='message_new',
        object=UpdateObject(message=Message(
            from_id=83106437,
            text='неверное слово',
            id=7172, payload=None)))

}


COMMANDS_USER2 = {
    "start": Update(
        type='message_new',
        object=UpdateObject(message=Message(
            from_id=12345678,
            text='Начать', id=7095,
            payload=Payload(command='start', letter=None)))),
    "game_request": Update(
        type='message_new',
        object=UpdateObject(message=Message(
            from_id=12345678,
            text='Отправить заявку на игру',
            id=7097,
            payload=Payload(command='game_request', letter=None)))),
    "about": Update(
        type='message_new',
        object=UpdateObject(message=Message(
            from_id=12345678,
            text='Об игре',
            id=7103,
            payload=Payload(command='about', letter=None)))),
    "start_game": Update(
        type='message_new',
        object=UpdateObject(message=Message(
            from_id=12345678,
            text='Играть',
            id=7107,
            payload=Payload(command='start_game', letter=None)))),
    "guess_letter": Update(
        type='message_new',
        object=UpdateObject(message=Message(
            from_id=12345678,
            text='п',
            id=7109,
            payload=Payload(command='guess_letter', letter='Рї')))),
    "quite": Update(
        type='message_new',
        object=UpdateObject(message=Message(
            from_id=12345678,
            text='Выйти из игры',
            id=7111,
            payload=Payload(command='quite', letter=None)))),
    "cancel_game_request": Update(
        type='message_new',
        object=UpdateObject(message=Message(
            from_id=12345678,
            text='Отменить заявку',
            id=7115,
            payload=Payload(command='cancel_game_request', letter=None)))),
    "начать": Update(
        type='message_new',
        object=UpdateObject(message=Message(
            from_id=12345678,
            text='начать',
            id=7117,
            payload=None)))
}
