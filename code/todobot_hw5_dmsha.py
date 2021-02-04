from random import choice
import telebot

token = ''
bot = telebot.TeleBot(token)

RANDOM_TASKS = ['Написать письмо Гвидо', 'Приготовить ужин', 'Просмотреть почту', 'Выучить Python'] 
todos = {}

HELP = """
Список доступных команд:
/help - вывести список доступных команд
/add - добавить задачу в список
/print - напечатать все задачи
/random - добавить случайную задачу на заданную дату
"""


def add_todo(date, task):
    date = date.lower()
    if todos.get(date) is not None:
        todos[date].append(task)
    else:
        todos[date] = [task]


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, HELP)


@bot.message_handler(commands=['random'])
def random(message):
    task = choice(RANDOM_TASKS)
    add_todo('сегодня', task)
    bot.send_message(message.chat.id, f'Задача "{task}" добавлена на "Сегодня"')


@bot.message_handler(commands=['add'])
def add_task(message):
    command = message.text.split(maxsplit=2)
    date = command[1]
    task = command[2]
    if len(task) < 3:
        bot.send_message(message.chat.id, f'Ошибка. Задача не может быть такой короткой...')
    else:
        add_todo(date, task)
        bot.send_message(message.chat.id, f'Задача "{task}" добавлена на "{date}"')


@bot.message_handler(commands=['print'])
def print_tasks(message):
    dates = message.text.split()
    for date in dates:
        date = date.lower()
        if date in todos:
            tasks = todos[date]
            text = date
            for task in tasks:
                text = text + f'\n[ ] {task}'
        else:
            text = f'На дату "{date}" - задач нет...'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
