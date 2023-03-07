from telegram import Update
from telegram.ext import CallbackContext as Context
from faunadb import query as q
from faunadb.client import FaunaClient
from utils import secret as f

client = FaunaClient(secret=f)

def my_booking(update: Update, context: Context) -> None:
   
   chat_id = update.effective_chat.id

   event_message = ""
   events = client.query(q.paginate(q.match(q.index("appointment_index"), chat_id)))
   for i in events["data"]:
       event = client.query(q.get(q.ref(q.collection("Appointments"), i.id())))
       event_message += "{}\nTime: {}\nDelete your booking: /unbook_{}\n\n".format(event["data"]["name"], event["data"]["time"], i.id())
   if event_message == "":
       event_message = "You still have no bookings, let's fix that with /booking 😇"
   context.bot.send_message(chat_id=chat_id, text=event_message)