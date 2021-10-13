from django.core.management.base import BaseCommand
from telegram import Bot, ReplyKeyboardMarkup
from telegram.ext import CommandHandler, ConversationHandler
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import Updater
from telegram.utils.request import Request
from django.conf import settings
import telegram
import httplib2
import csv
import os
import os.path
from io import StringIO
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials

from main.models import Users, Product


CREDENTIALS_FILE = 'creds.json'
spreadsheet_id = '1-1_yVsyktQXCOXk2rSEDWUe2tUeVXcg5G2EgeE-RjY0'

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    ['https://www.googleapis.com/auth/spreadsheets',
     'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)

values = service.spreadsheets().values().get(
    spreadsheetId=spreadsheet_id,
    range='A1:G17',
).execute()
value = values.get('values', [])

dir = r"/home/maksym/Doc/Git/test_bot/telebot"
if not os.path.exists(dir):
    os.mkdir(dir)

with open(os.path.join(dir, "filename" + '.csv'), "w") as f:
    csvfile = StringIO()
    csvwriter = csv.writer(csvfile)
    for lm in value:
        csvwriter.writerow(lm)
    for al in csvfile.getvalue():
        f.writelines(al)


FirstName, LastName, Phone, Gallery = range(4)

reply_keyboard = [['Каталог']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
bot = telegram.Bot(token=settings.TOKEN)


def start(update, context):
    with open("filename.csv", encoding='utf-8') as r_file:
        file_reader = csv.DictReader(r_file, delimiter=",")
        count = 0
        for row in file_reader:
            user = Product(
                id=row["id"],
                name=row['name'],
                qty=row['qty'],
                desc=row['desc'],
                price=row['price'],
                img=row['img'],
                availability=row['availability']
            )
            user.save()
            count += 1
    print(count)
    update.message.reply_text('Ваше имя?')

    return FirstName


def first_name(update, context):
    firstname = update.message.text
    chat_id = update.message.chat_id
    try:
        obj, created = Users.objects.update_or_create(
            tele_id=chat_id,
            defaults={'first_name': firstname},
        )
        update.message.reply_text('Ваша Фамилия?')
        return LastName
    except: # noqa
        update.message.reply_text('Что-то не так, попробуй ещё раз ввести имя.')
        return FirstName


def last_name(update, context):
    lastname = update.message.text
    chat_id = update.message.chat_id
    try:
        obj, created = Users.objects.update_or_create(
            tele_id=chat_id,
            defaults={'last_name': lastname}
        )
        update.message.reply_text('Ваш Телефон?')
        return Phone
    except: # noqa
        update.message.reply_text('Что-то не так, попробуй ещё раз ввести фамилию.')
        return LastName


def phone(update, context):
    phin = update.message.text
    chat_id = update.message.chat_id
    try:
        obj, created = Users.objects.update_or_create(
            tele_id=chat_id,
            defaults={'phone': phin}
        )
        update.message.reply_text('Отлично, ты прошёл регистрацию!', reply_markup=markup)
        return Gallery
    except: # noqa
        update.message.reply_text('Что-то не так, попробуй ещё раз ввести телефон.')
        return Phone


def gallery(update, context):
    chat_id = update.message.chat_id
    posts = Product.objects.all()

    for post in posts:
        bot.send_photo(chat_id=chat_id, photo=post.img)
        update.message.reply_text(f'Название: {post.name}\nОписание: {post.desc}\nЦена: {post.price}')

    return ConversationHandler.END


def cancel(update, context):
    update.message.reply_text(
        'Пока, было приятно пообщаться')

    return ConversationHandler.END


class Command(BaseCommand):
    help = "Telegramm bot"

    def handle(self, *args, **options):
        request = Request(
            connect_timeout=1,
            read_timeout=2.0,
        )
        bot = Bot(
            request=request,
            token=settings.TOKEN,
        )
        print(bot.get_me())

        updater = Updater(
            bot=bot,
        )

        dispatcher = updater.dispatcher

        conv_handler = ConversationHandler(
            entry_points=[CommandHandler("start", start)],
            states={
                FirstName: [MessageHandler(Filters.text, first_name)],
                LastName: [MessageHandler(Filters.text, last_name)],
                Phone: [MessageHandler(Filters.text, phone)],
                Gallery: [MessageHandler(Filters.regex('^Каталог$'), gallery)]
            },

            fallbacks=[CommandHandler('cancel', cancel)]
        )

        dispatcher.add_handler(conv_handler)

        updater.start_polling()
        updater.idle()


if __name__ == '__main__':
    main() # noqa
