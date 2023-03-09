from telegram import Update
from telegram.ext import ConversationHandler, CallbackContext as Context
from faunadb import query as q
from faunadb.client import FaunaClient
from modules.up_states import SELECTION
from utils import secret as f 

client = FaunaClient(secret=f)

def upbook(update: Update, context: Context) -> None:
   chat_id = update.effective_chat.id
   user = client.query(q.get(q.match(q.index("users_index"), chat_id)))
   booked = user["data"]["booked"]

   if not booked:
      context.bot.send_message(chat_id, "You have no appointments. Use /booking")
      return ConversationHandler.END
   else:
      context.bot.send_message(chat_id, "What do you want to update? Name, instruments, time or mobile number?")
      client.query(q.update(q.ref(q.collection("Users"), user["ref"].id()),
                              {"data": {"last_command": "upbook"}}))
      return SELECTION


