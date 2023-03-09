from telegram import Update
from telegram.ext import ConversationHandler
from telegram.ext import CallbackContext as Context
from faunadb import query as q
from faunadb.client import FaunaClient
from utils import group_id, secret as f
from modules.echo import echo

SELECTION = 0
BAND_NAME = 1
INSTRUMENTS = 2
TIME_SET = 3
MOBILE_NUM = 4
DONE = 5

p_name = ""
p_instr = ""
p_time = 0
p_mobile = 0
restore = 0

client = FaunaClient(secret=f)

def selection(update: Update, context: Context) -> None:
    chat_id = update.effective_chat.id 
    message = update.message.text

    if message.lower() == "name":
        context.bot.send_message(chat_id, "What's your band name?")
        return BAND_NAME
    if message.lower() == "instrument" or message.lower() == "instruments":
        context.bot.send_message(chat_id, "What are your instruments?")
        return INSTRUMENTS
    if message.lower() == "time":
        context.bot.send_message(chat_id, "When do you want to play?")
        return TIME_SET
    if message.lower() == "mobile":
        context.bot.send_message(chat_id, "What's your mobile phone?")
        return MOBILE_NUM

    context.bot.send_message(chat_id, "Invalid input, try again!")


def band_name(update: Update, context: Context) -> None:
    chat_id = update.effective_chat.id
    message = update.message.text
    global p_name
    global restore
    event = client.query(q.get(q.match(q.index("appointment_index"), chat_id)))
    p_name = client.query(q.select("name", event["data"]))
    client.query(q.update(q.ref(q.collection("Appointments"), event["ref"].id()), {"data": {"name": message}}))
    restore = 1
    context.bot.send_message(chat_id, "Are you sure you want update your information?")
    return DONE

def instruments(update: Update, context: Context) -> None:
    chat_id = update.effective_chat.id
    message = update.message.text
    global p_instr
    global restore
    event = client.query(q.get(q.match(q.index("appointment_index"), chat_id)))
    p_instr = client.query(q.select("instrument", event["data"]))
    client.query(q.update(q.ref(q.collection("Appointments"), event["ref"].id()), {"data": {"instrument": message}}))
    restore = 2
    context.bot.send_message(chat_id, "Are you sure you want update your information?")
    return DONE

def time_set(update: Update, context: Context) -> None:
    chat_id = update.effective_chat.id
    message = update.message.text
    global p_time
    global restore
    event = client.query(q.get(q.match(q.index("appointment_index"), chat_id)))
    p_time = client.query(q.select("time", event["data"]))
    client.query(q.update(q.ref(q.collection("Appointments"), event["ref"].id()), {"data": {"time": message}}))
    restore = 3
    context.bot.send_message(chat_id, "Are you sure you want update your information?")
    return DONE

def mobile_num(update: Update, context: Context) -> None:
    chat_id = update.effective_chat.id
    message = update.message.text
    global p_mobile
    global restore
    event = client.query(q.get(q.match(q.index("appointment_index"), chat_id)))
    p_mobile = client.query(q.select("mobile", event["data"]))
    client.query(q.update(q.ref(q.collection("Appointments"), event["ref"].id()), {"data": {"mobile": message}}))
    restore = 4
    context.bot.send_message(chat_id, "Are you sure you want update your information? Yes or No")
    return DONE

def done(update: Update, context: Context) -> None:
    chat_id = update.effective_chat.id
    message = update.message.text
    user = client.query(q.get(q.match(q.index("users_index"), chat_id)))

    if message.lower() == "yes":
        context.bot.send_message(chat_id, "Your information has been updated!")
        context.bot.send_message(group_id, "A client has been updated their info:")
        client.query(q.update(q.ref(q.collection("Users"), user["ref"].id()),
                              {"data": {"last_command": "upbook"}}))
        echo(update, context)
        return ConversationHandler.END
    elif message.lower() == "no":
        if restore == 1:
            event = client.query(q.get(q.match(q.index("appointment_index"), chat_id)))
            client.query(q.update(q.ref(q.collection("Appointments"), event["ref"].id()), {"data": {"name": p_name}}))
            context.bot.send_message(chat_id, "Your informations have been restored!")
            return ConversationHandler.END
        elif restore == 2:
            event = client.query(q.get(q.match(q.index("appointment_index"), chat_id)))
            client.query(q.update(q.ref(q.collection("Appointments"), event["ref"].id()), {"data": {"instrument": p_instr}}))
            context.bot.send_message(chat_id, "Your informations have been restored!")
            return ConversationHandler.END
        elif restore == 3:
            event = client.query(q.get(q.match(q.index("appointment_index"), chat_id)))
            client.query(q.update(q.ref(q.collection("Appointments"), event["ref"].id()), {"data": {"time": p_time}}))
            context.bot.send_message(chat_id, "Your informations have been restored!")
            return ConversationHandler.END
        elif restore == 4:
            event = client.query(q.get(q.match(q.index("appointment_index"), chat_id)))
            client.query(q.update(q.ref(q.collection("Appointments"), event["ref"].id()), {"data": {"mobile": p_mobile}}))
            context.bot.send_message(chat_id, "Your informations have been restored!")
            return ConversationHandler.END

    context.bot.send_message(chat_id , "Invalid input!")







