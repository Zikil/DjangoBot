from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from djbot.models import *
import os 
from telegram.ext import Updater, CommandHandler
from telegram.ext import MessageHandler, Filters, InlineQueryHandler

TOKEN = '1033970790:AAHgVbhB3yDw38jC4CIiEoi6jzbP5k_h0HQ'
baselink = os.getcwd() + '/media/tb/'

groups_tb = {'ИПМИ-20': baselink + 'ИИТиАС_2.pdf', 'ИПМИ-21': baselink + 'ИИТиАС_1.pdf'}

def add_message(update):
    chat_id = update.message.chat_id
    text = update.message.text
    p, _ = Profile.objects.get_or_create(
        external_id=chat_id,
        defaults={
            'name': update.message.from_user.username,
        }
    )
    m = Message(
        profile=p,
        text=text,
    )
    m.save()

class Command(BaseCommand):
    updater = Updater(token=TOKEN)
    dispatcher = updater.dispatcher

    # функция обработки команды '/start'
    def start(update, context):
        chat_id = update.message.chat_id
        text = update.message.text
        context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")
        p, _ = Profile.objects.get_or_create(
            external_id=chat_id,
            defaults={
                'name': update.message.from_user.username,
            }
        ) 
        # m = Message(
        #     profile=p,
        #     text=text,
        # )
        # m.save()

    def all_groups(update, context):
        text = ''
        g = Groups.objects.all().values('name')
        for g1 in g:
            text = text + g1.get('name') + '\n'
        context.bot.send_message(chat_id=update.effective_chat.id, text=text)

    def all_timetables(update, context):
        text = ''
        t = Timetable.objects.all().values('name')
        for t1 in t:
            text = text + t1.get('name') + '\n'
        context.bot.send_message(chat_id=update.effective_chat.id, text=text)
 
    # функция обработки текстовых сообщений
    def echo(update, context):
        text = update.message.text
        if Groups.objects.filter(name = text):
            g = Groups.objects.filter(name = text).values('name').get().get('name')
            link_id = Groups.objects.filter(name = g).values('tb_id').get().get('tb_id')
            link = baselink + Timetable.objects.filter(id = link_id).values('link').get().get('link')
            context.bot.send_document(chat_id=update.effective_chat.id, document=open(link, 'rb'))
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text=text)
            add_message(update)

    # функция обработки не распознных команд
    def unknown(update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

    # обработчик команды '/start'
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)    
    
    #вывод всех групп
    all_handler = CommandHandler('allgroups', all_groups)
    dispatcher.add_handler(all_handler)

    #вывод всех расписаний
    all_handler = CommandHandler('alltb', all_timetables)
    dispatcher.add_handler(all_handler)

    # обработчик текстовых сообщений
    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    dispatcher.add_handler(echo_handler)

    # обработчик не распознных команд
    unknown_handler = MessageHandler(Filters.command, unknown)
    dispatcher.add_handler(unknown_handler)

    # запуск прослушивания сообщений
    updater.start_polling()
    # обработчик нажатия Ctrl+C
    updater.idle()
