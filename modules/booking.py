from telegram import Update
from telegram.ext import ConversationHandler, CallbackContext as Context
from faunadb import query as q
from faunadb.client import FaunaClient
from modules.states import CONF
from utils import secret as f

client = FaunaClient(secret=f)


def booking(update: Update, context: Context) -> None:

    chat_id = update.effective_chat.id
    user = client.query(q.get(q.match(q.index("users_index"), chat_id)))
    booked = user["data"]["booked"]

    if not booked:
        client.query(q.update(q.ref(q.collection("Users"), user["ref"].id()), 
                              {"data": {"last_command": "booking"}}))
        client.query(q.update(q.ref(q.collection("Users"), user["ref"].id()), 
                              {"data": {"booked": True}}))
        client.query(q.create(q.collection("Appointments"), {
            "data": {
                "index": chat_id,
                "name": "",
                "instrument": "",
                "time": "",
                "mobile": "",
            }
        }))
        context.bot.send_message(chat_id, 
                                 "Do you wanna confirm? Answer with either yes or no.")

        return CONF
    
    context.bot.send_message(chat_id, "You are already booked")
    return ConversationHandler.END