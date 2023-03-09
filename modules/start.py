from datetime import datetime
from telegram import Update
from telegram.ext import CallbackContext as Context
import pytz
from faunadb import query as q
from faunadb.client import FaunaClient
from utils import secret as f

client = FaunaClient(secret=f)


def start(update: Update, context: Context) -> None:
    chat_id = update.effective_chat.id
    first_name = update["message"]["chat"]["first_name"]
    username = update["message"]["chat"]["username"]

    try:
        client.query(q.get(q.match(q.index("users_index"), chat_id)))
        context.bot.send_message(chat_id=chat_id, text="Welcome to our booking bot! \n\n To book an appointment /booking \n To see your booking /my_booking \n To update your information /upbook \n The studio is available at 6 PM and 8 PM")
    except:
        client.query(q.create(q.collection("Users"), {
            "data": {
                "index": chat_id,
                "first_name": first_name,
                "username": username,
                "last_command": "",
                "booked": False,
                "date": datetime.now(pytz.UTC)
            }
        }))
    
    context.bot.send_message(chat_id=chat_id, text="Welcome to our booking bot! \n\n To book an appointment /booking \n To see your booking /my_booking \n The studio is available at 6 PM and 8 PM")
