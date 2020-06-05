from django.core.management.base import BaseCommand
from django.conf import settings
from telegram import Bot, Update
from telegram.ext import CallbackContext, Filters, Updater
from telegram.ext import CommandHandler, MessageHandler
from telegram.utils.request import Request

from ugc.models import Profile, Message


def log_errors(f):
    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            error_message = f'Error: {e}'
            print(error_message)
            raise e
    return inner


@log_errors
def do_echo(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    text = update.message.text
    print('Echo')
    p, _ = Profile.objects.get_or_create(
        external_id=chat_id,
        defaults={
            'name': update.message.from_user.username
        }
    )
    m = Message(
        profile=p,
        text=text
    )
    m.save()
    reply_text = f'Your ID: {chat_id}\nMessage ID: {m.pk}\n{text}'
    update.message.reply_text(
        text=reply_text
    )


@log_errors
def do_count(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    print('Count')
    p, _ = Profile.objects.get_or_create(
        external_id=chat_id,
        defaults={
            'name': update.message.from_user.username
        }
    )
    count = Message.objects.filter(profile=p).count()

    reply_text = f'You sent {count} message'
    update.message.reply_text(
        text=reply_text
    )


class Command(BaseCommand):
    help = 'Telegram-bot'

    def handle(self, *args, **options):
        request = Request(
            connect_timeout=10,
            read_timeout=10
        )
        bot = Bot(
            request=request,
            token=settings.TOKEN,
            base_url=settings.PROXY_URL
        )
        updater = Updater(
            bot=bot,
            use_context=True
        )

        message_handler2 = CommandHandler('count', do_count)
        updater.dispatcher.add_handler(message_handler2)

        message_handler = MessageHandler(Filters.text, do_echo)
        updater.dispatcher.add_handler(message_handler)

        print('Done\nStart polling...')
        updater.start_polling()
        updater.idle()
