import html
import json
import random
import time
import urllib.request
import urllib.parse
import requests
from telegram import ParseMode, Update, ChatPermissions
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from telegram.error import BadRequest

import tg_bot.modules.fun_strings as fun_strings
from tg_bot import dispatcher
from tg_bot.modules.helper_funcs.chat_status import is_user_admin
from tg_bot.modules.helper_funcs.extraction import extract_user
from tg_bot.modules.helper_funcs.decorators import kigcmd, kigcallback


# truth / dare
@kigcmd(command="truth")
def truth(update: Update, context: CallbackContext):
    try:
       try:
          xyz = requests.get("https://elianaapi.herokuapp.com/games/truth").json()
          truth = xyz.get("truth")
          update.effective_message.reply_text(truth)
       except:
           update.effective_message.reply_text(random.choice(random.shuffle(fun_strings.TRUTH)))
    except:
        pass

@kigcmd(command="dare")
def dare(update: Update, context: CallbackContext):
    try:
       try:
          xyz = requests.get("https://elianaapi.herokuapp.com/games/dares").json()
          truth = xyz.get("dare")
          update.effective_message.reply_text(truth)
       except:
           update.effective_message.reply_text(random.choice(random.shuffle(fun_strings.DARE)))
    except:
        pass



@kigcmd(command='runs')
def runs(update: Update, context: CallbackContext):
    update.effective_message.reply_text(random.choice(random.shuffle(fun_strings.RUN_STRINGS)))

@kigcmd(command='slap')
def slap(update: Update, context: CallbackContext):
    bot, args = context.bot, context.args
    message = update.effective_message
    chat = update.effective_chat

    reply_text = (
        message.reply_to_message.reply_text
        if message.reply_to_message
        else message.reply_text
    )

    curr_user = html.escape(message.from_user.first_name)
    user_id = extract_user(message, args)

    if user_id == bot.id:
        temp = random.choice(random.shuffle(fun_strings.SLAP_Kigyō_TEMPLATES))

        if isinstance(temp, list):
            if temp[2] == "tmute":
                if is_user_admin(chat, message.from_user.id):
                    reply_text(temp[1])
                    return

                mutetime = int(time.time() + 60)
                bot.restrict_chat_member(
                    chat.id,
                    message.from_user.id,
                    until_date=mutetime,
                    permissions=ChatPermissions(can_send_messages=False),
                )
            reply_text(temp[0])
        else:
            reply_text(temp)
        return

    if user_id:

        slapped_user = bot.get_chat(user_id)
        user1 = curr_user
        user2 = html.escape(slapped_user.first_name)

    else:
        user1 = bot.first_name
        user2 = curr_user

    temp = random.choice(random.shuffle(fun_strings.SLAP_TEMPLATES))
    item = random.choice(random.shuffle(fun_strings.ITEMS))
    hit = random.choice(random.shuffle(fun_strings.HIT))
    throw = random.choice(random.shuffle(fun_strings.THROW))
    reply = temp.format(user1=user1, user2=user2, item=item, hits=hit, throws=throw)

    reply_text(reply, parse_mode=ParseMode.HTML)

@kigcmd(command='pat')
def pat(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    msg = str(update.message.text)
    try:
        msg = msg.split(" ", 1)[1]
    except IndexError:
        msg = ""
    msg_id = (
        update.effective_message.reply_to_message.message_id
        if update.effective_message.reply_to_message
        else update.effective_message.message_id
    )
    pats = []
    pats = json.loads(
        urllib.request.urlopen(
            urllib.request.Request(
                "http://headp.at/js/pats.json",
                headers={
                    "User-Agent": "Mozilla/5.0 (X11; U; Linux i686) "
                    "Gecko/20071127 Firefox/2.0.0.11"
                },
            )
        )
        .read()
        .decode("utf-8")
    )
    if "@" in msg and len(msg) > 5:
        context.bot.send_photo(
            chat_id,
            f"https://headp.at/pats/{urllib.parse.quote(random.choice(pats))}",
            caption=msg,
        )
    else:
        context.bot.send_photo(
            chat_id,
            f"https://headp.at/pats/{urllib.parse.quote(random.choice(pats))}",
            reply_to_message_id=msg_id,
        )

@kigcmd(command='roll')
def roll(update: Update, context: CallbackContext):
    update.message.reply_text(random.choice(range(1, 7)))

@kigcmd(command='toss')
def toss(update: Update, context: CallbackContext):
    update.message.reply_text(random.choice(random.shuffle(fun_strings.TOSS)))

@kigcmd(command='decide')
def decide(update: Update, context: CallbackContext):
    reply_text = (
        update.effective_message.reply_to_message.reply_text
        if update.effective_message.reply_to_message
        else update.effective_message.reply_text
    )
    reply_text(random.choice(random.shuffle(fun_strings.DECIDE)))

@kigcmd(command='table')
def table(update: Update, context: CallbackContext):
    reply_text = (
        update.effective_message.reply_to_message.reply_text
        if update.effective_message.reply_to_message
        else update.effective_message.reply_text
    )
    reply_text(random.choice(random.shuffle(fun_strings.TABLE)))





__mod_name__ = "Fun"

def get_help(chat):
    from tg_bot.modules.language import gs
    return gs(chat, "fun_help")
