from telegram.ext import Updater
from telegram.ext import CommandHandler, ConversationHandler
from telegram.ext import MessageHandler, Filters
from faunadb.client import FaunaClient
from utils import telegram_bot_token as t, secret as f
from modules.booking import booking
from modules.unbook import unbook
from modules.echo import echo
from modules.my_booking import my_booking
from modules.start import start
from modules.upbook import upbook
from modules.states import confirmation, name, instrument, time, mobile, end, CONF, NAME, INSTRUMENT, TIME, MOBILE, END
from modules.up_states import selection, band_name, instruments, time_set, mobile_num, done, SELECTION, BAND_NAME, INSTRUMENTS, TIME_SET, MOBILE_NUM, DONE


client = FaunaClient(secret=f)
updater = Updater(token=t, use_context=True)
dispatcher = updater.dispatcher


handler = ConversationHandler(
    entry_points=[CommandHandler('booking', booking)],
    states={
            CONF: [MessageHandler(Filters.text, confirmation)],
            NAME: [MessageHandler(Filters.text, name)],
            INSTRUMENT: [MessageHandler(Filters.text, instrument)],
            TIME: [MessageHandler(Filters.text, time)],
            MOBILE: [MessageHandler(Filters.text, mobile)],
            END: [MessageHandler(Filters.text, end)],
    },
    fallbacks=[None]
)

updating = ConversationHandler(
    entry_points=[CommandHandler('upbook', upbook)],
    states={
            SELECTION: [MessageHandler(Filters.text, selection)],
            BAND_NAME: [MessageHandler(Filters.text, band_name)],
            INSTRUMENTS: [MessageHandler(Filters.text, instruments)],
            TIME_SET: [MessageHandler(Filters.text, time_set)],
            MOBILE_NUM: [MessageHandler(Filters.text, mobile_num)],
            DONE: [MessageHandler(Filters.text, done)],
    },
    fallbacks=[None]
)


dispatcher.add_handler(handler)
dispatcher.add_handler(updating)
dispatcher.add_handler(CommandHandler("my_booking", my_booking))
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(Filters.regex("/unbook_[0-9]*"), unbook))
dispatcher.add_handler(MessageHandler(Filters.text, echo))
updater.start_polling()

updater.idle()
