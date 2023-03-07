from telegram import Update
from telegram.ext import CallbackContext as Context
from faunadb import query as q
from faunadb.client import FaunaClient
from utils import group_id, secret as f



client = FaunaClient(secret=f)

def unbook(update: Update, context: Context) -> None:
   
   chat_id = update.effective_chat.id
   message = update.message.text
   event_id = message.split("_")[1]
   event = client.query(q.get(q.match(q.index("appointment_index"), chat_id)))
   user = client.query(q.get(q.match(q.index("users_index"), chat_id)))
   client.query(q.update(q.ref(q.collection("Users"), user["ref"].id()), 
                         {"data": {"booked": False}}))

   client.query(q.delete(q.ref(q.collection("Appointments"), event_id)))
   context.bot.send_message(group_id, "Client " +
                            event["data"]["name"] + 
                            " has deleted their appointment.")
   context.bot.send_message(chat_id=chat_id, text="Your appointment has been succesfully removed!")