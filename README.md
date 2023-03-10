# Telegram Booking Bot

This simple telegram bot is made as a booking/scheduler system for various activities. This example is made for a recording studio.
In the near future i'll implement the bot with google calendar and i'll add the possibility to view the empty slots.
The bot records the bookings and client to a DB with Fauna.


## Fauna Setup

Head to https://fauna.com and create your account and database. Create two collections, named "Appointments" and "Users".
In the Users collection create an index named "users_index" and in the Appointment collection create "appointment_index".


## Installation

The projects runs with Python 3.8.10 or 3.9 and python-telegram-bot 13.7. You'll need faunadb APIs, pytz and telegram too.


 ```
 pip install python-telegram-bot==13.7
 pip install telegram
 pip install faunadb
 pip install pytz
 ```

## Usage

Go to the "utils.py" file and put your telegram bot token that you generated from BotFather in "telegram_bot_token".
In "secret" you need to type the faunadb token and in "group_id" the chat_id of the group or chat you want the bot to send the message.
Of course if you want to use a group be sure to add the bot in it before running the script.

To run the project open a terminal in the directory and run:

```
python main.py
```

The commands and methods can be found in the modules/ directory.


## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D