from telegram import Update
from telegram.ext import ConversationHandler
from telegram.ext import CallbackContext as Context
from faunadb import query as q
from faunadb.client import FaunaClient
from utils import secret as f
from modules.echo import echo

CONF = 0
NAME = 1
INSTRUMENT = 2
TIME = 3
MOBILE = 4
END = 5


client = FaunaClient(secret=f)



def confirmation(update: Update, context: Context) -> None:
    chat_id = update.effective_chat.id 
    message = update.message.text

    if message.lower() == "yes":
        context.bot.send_message(chat_id, "What's your band name?")
        return NAME
    if message.lower() == "no":
        chat_id = update.effective_chat.id 
        context.bot.send_message(chat_id, "Deleting your appointment...")
        user = client.query(q.get(q.match(q.index("users_index"), chat_id)))
        client.query(q.update(q.ref(q.collection("Users"), user["ref"].id()), {"data": {"last_command": ""}}))
        client.query(q.update(q.ref(q.collection("Users"), user["ref"].id()), {"data": {"booked": False}}))
        event = client.query(q.get(q.match(q.index("appointment_index"), chat_id)))
        client.query(q.delete(q.ref(q.collection("Appointments"), event["ref"].id())))
        context.bot.send_message(chat_id, "Booking deleted, see you soon!")
        return ConversationHandler.END
    
    context.bot.send_message(chat_id, "Invalid message, try again please...")


def name(update: Update, context: Context) -> None:
    chat_id = update.effective_chat.id 
    message = update.message.text
    event = client.query(q.get(q.match(q.index("appointment_index"), chat_id)))
    client.query(q.update(q.ref(q.collection("Appointments"), event["ref"].id()), {"data": {"name": message}}))
    context.bot.send_message(chat_id, "What instruments do you all play?")
    return INSTRUMENT



def instrument(update: Update, context: Context) -> None:
    chat_id = update.effective_chat.id
    message = update.message.text
    event = client.query(q.get(q.match(q.index("appointment_index"), chat_id)))
    client.query(q.update(q.ref(q.collection("Appointments"), event["ref"].id()), {"data": {"instrument": message}}))
    context.bot.send_message(chat_id, "What's the time you prefer?")
    return TIME
    


def time(update: Update, context: Context) -> None:
    chat_id = update.effective_chat.id
    message = update.message.text
    event = client.query(q.get(q.match(q.index("appointment_index"), chat_id)))
    client.query(q.update(q.ref(q.collection("Appointments"), event["ref"].id()), {"data": {"time": message}}))
    context.bot.send_message(chat_id, "What's your mobile number?")
    return MOBILE
    


def mobile(update: Update, context: Context) -> None: 
    chat_id = update.effective_chat.id
    message = update.message.text
    event = client.query(q.get(q.match(q.index("appointment_index"), chat_id)))
    client.query(q.update(q.ref(q.collection("Appointments"), event["ref"].id()), {"data": {"mobile": message}}))
    context.bot.send_message(chat_id, "Do you want to confirm the appointment? Answer with yer or no:")
    return END
    


def end(update: Update, context: Context) -> None:
    chat_id = update.effective_chat.id 
    message = update.message.text

    if message.lower() == "yes":
        context.bot.send_message(chat_id, "Thank you for your booking, we'll let you know soon")
        echo(update, context)
        return ConversationHandler.END
    if message.lower() == "no":
        chat_id = update.effective_chat.id
        context.bot.send_message(chat_id, "Deleting your appointment...")
        user = client.query(q.get(q.match(q.index("users_index"), chat_id)))
        client.query(q.update(q.ref(q.collection("Users"), user["ref"].id()), {"data": {"last_command": ""}}))
        client.query(q.update(q.ref(q.collection("Users"), user["ref"].id()), {"data": {"booked": False}}))
        event = client.query(q.get(q.match(q.index("appointment_index"), chat_id)))
        client.query(q.delete(q.ref(q.collection("Appointments"), event["ref"].id())))
        context.bot.send_message(chat_id, "Booking deleted, see you soon!")
        return ConversationHandler.END
    
    context.bot.send_message(chat_id, "Invalid message, try again please...")
    
    