from telegram import Update
from telegram.ext import CallbackContext as Context
from faunadb import query as q
from faunadb.client import FaunaClient
from utils import group_id, secret as f


client = FaunaClient(secret=f)



def echo(update: Update, context: Context) -> None:
    chat_id = update.effective_chat.id
    message = update.message.text

    if chat_id != group_id:

        user = client.query(q.get(q.match(q.index("users_index"), chat_id)))
        last_command = user["data"]["last_command"]
        global p_chat_id

        if last_command == "booking":
            p_chat_id = chat_id
            event = client.query(q.get(q.match(q.index("appointment_index"), p_chat_id)))
            client.query(q.update(q.ref(q.collection("Users"), user["ref"].id()), 
                                  {"data": {"last_command": ""}}))
            client.query(q.update(q.ref(q.collection("Users"), user["ref"].id()), 
                                  {"data": {"booked": True}}))
            name = client.query(q.select("name", event["data"]))
            instrument = client.query(q.select("instrument", event["data"]))
            time = client.query(q.select("time", event["data"]))
            mobile = client.query(q.select("mobile", event["data"]))
            context.bot.send_message(group_id, "Band Name: " + str(name) + "\n\n" + "Instruments: " + str(instrument) + "\n\n" + "Time: " +
                                     str(time) + "\n\n" + "Mobile number: " + str(mobile) + "\n\n" + "Client ID " + str(p_chat_id))
            context.bot.send_message(group_id, "To confirm type '/accept <Client ID>' and to refuse '/refuse <Client ID>'")
            

            
    elif chat_id == group_id and message.split(" ")[0] == "/accept":
        n_id = message.split(" ")[1]
        try:
            client.query(q.get(q.match(q.index("appointment_index"), int(n_id))))
            context.bot.send_message(group_id, "The Appointment has been approved!")
            context.bot.send_message(chat_id=(message.split(" ")[1]), text="Your request has been approved!")
            context.bot.send_message(chat_id=(message.split(" ")[1]), text="If you wanna see the details of your booking or delete it tap: " +
                                     "\n\n" + "/my_booking")
        except:
            context.bot.send_message(group_id, "Incorrect Client ID, try again")

    elif chat_id == group_id and message.split(" ")[0] == "/refuse":
            n_id = message.split(" ")[1]
            user = client.query(q.get(q.match(q.index("users_index"), int(n_id))))
            try:
                client.query(q.get(q.match(q.index("appointment_index"), int(n_id))))
                event = client.query(q.get(q.match(q.index("appointment_index"), int(n_id))))
                client.query(q.delete(q.ref(q.collection("Appointments"), event["ref"].id())))
                client.query(q.update(q.ref(q.collection("Users"), user["ref"].id()), {"data": {"booked": False}}))
                context.bot.send_message(group_id, text="The Appointment has been refused")
                context.bot.send_message(chat_id=(message.split(" ")[1]), text="Your appointment has been refused, try another time...")
            except:
                context.bot.send_message(group_id, "Incorrect Client ID, try again")
