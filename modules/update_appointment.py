from telegram import Update
from telegram.ext import CallbackContext as Context
from faunadb import query as q
from faunadb.client import FaunaClient
from utils import secret as f 

client = FaunaClient(secret=f)

def update_appointment(update: Update, context: Context) -> None:
   chat_id = update.effective_chat.id
   message = update.message.text
   event_id = message.split("_")[1]

   event = client.query(q.get(q.ref(q.collection("Appointments"), event_id)))
   if event["data"]["completed"]:
       new_status = not event["data"]["completed"]
   else:
       new_status = True
   client.query(q.update(q.ref(q.collection("Appointments"), event_id), {"data": {"completed": new_status}}))
   context.bot.send_message(chat_id=chat_id, text="Successfully updated appointment status 👌")