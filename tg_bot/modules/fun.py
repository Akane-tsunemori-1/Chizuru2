import html
import json
import random
import time
import urllib.request
import urllib.parse
import requests

from telegram import ParseMode, Update, ChatAction, ChatPermissions
from telegram.ext import Filters, CallbackContext
from telegram.error import BadRequest

from tg_bot.modules.helper_funcs.decorators import kigcmd, kigmsg
from tg_bot.modules.helper_funcs.chat_status import is_user_admin
from tg_bot.modules.helper_funcs.extraction import extract_user
import tg_bot.modules.fun_strings as fun


@kigcmd(command='runs')
def runs(update, context):
    update.effective_message.reply_text(random.choice(fun.RUN_STRINGS))


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
        temp = random.choice(fun.SLAP_BOT_TEMPLATES)

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

    temp = random.choice(fun.SLAP_TEMPLATES)
    item = random.choice(fun.ITEMS)
    hit = random.choice(fun.HIT)
    throw = random.choice(fun.THROW)
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
    pat_type = random.choice(("Photo", "Gif"))
    if pat_type == "Photo":
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
        try:
            context.bot.send_chat_action(update.effective_chat.id, action=ChatAction.UPLOAD_PHOTO)
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
        except BadRequest:
            return
    if pat_type == "Gif":
        try:
            context.bot.send_chat_action(update.effective_chat.id, action=ChatAction.UPLOAD_DOCUMENT)
            pat = requests.get('https://some-random-api.ml/animu/pat').json()
            if "@" in msg and len(msg) > 5:
                context.bot.send_animation(
                    chat_id,
                    pat.get('link'),
                    caption=msg,
                )
            else:
                context.bot.send_animation(
                    chat_id,
                    pat.get('link'),
                    reply_to_message_id=msg_id,
                )
        except BadRequest:
            return


@kigcmd(command='hug')
def hug(update: Update, context: CallbackContext):
    reply_animation = (
        update.effective_message.reply_to_message.reply_text
        if update.effective_message.reply_to_message
        else update.effective_message.reply_text
    )
    hug = requests.get('https://some-random-api.ml/animu/hug').json()
    reply_animation(hug.get('link'))


@kigcmd(command='decide')
def yesnowtf(update: Update, context: CallbackContext):
    msg = update.effective_message
    chat = update.effective_chat
    res = requests.get("https://yesno.wtf/api")
    if res.status_code != 200:
         msg.reply_text(random.choice(fun.DECIDE))
         return
    else:
        res = res.json()
    try:
        context.bot.send_animation(
            chat.id, animation=res.get("image"), caption=str(res.get("answer")).upper()
        )
    except BadRequest:
        return


@kigmsg(Filters.regex(r"(?i)^Chizuru\?"), friendly="decide")
def decide(update: Update, context: CallbackContext):
    reply_text = (
        update.effective_message.reply_to_message.reply_text
        if update.effective_message.reply_to_message
        else update.effective_message.reply_text
    )
    reply_text(random.choice(fun.DECIDE))



def get_help(chat):
    from tg_bot.modules.language import gs
    return gs(chat, "fun_help")

__mod_name__ = "Fun"
