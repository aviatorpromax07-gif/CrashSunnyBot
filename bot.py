import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
import random
import re
import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

# আপনার বটের টোকেন
TOKEN = '8276327075:AAHA-7nrNfRhLCauU90xfuXV3-v2vhiURdE'
bot = telebot.TeleBot(TOKEN)

# অ্যাডমিনদের ইউজারনেম
ADMINS =['@SPECIAL_7_9', '@SUNNY_BRO1']

# ওয়েব অ্যাপ লিংক এবং ওয়েলকাম ইমেজের লিংক
WEB_APP_URL = 'https://crashsunny.netlify.app/'
IMAGE_URL = 'https://i.ibb.co.com/qFmpJZqz/photo-ghost.jpg' 

# ইউজারদের স্টেট সেভ রাখার ডিকশনারি
user_states = {}

# -------- Render এর জন্য Dummy Web Server --------
class DummyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"Telegram Bot is running smoothly!")

def run_dummy_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), DummyHandler)
    server.serve_forever()

# ব্যাকগ্রাউন্ড থ্রেডে সার্ভার চালু করা
threading.Thread(target=run_dummy_server, daemon=True).start()
# -------------------------------------------------

# /start কমান্ড হ্যান্ডলার
@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    
    # আপনার নতুন ওয়েলকাম মেসেজ
    text = """Welcome to our Bot!

🍎 Apple Win Pro – The smartest AI Bot for Apple of Fortune!
💡 Get accurate signals, fast updates, and easy wins.

👻 Powered by Ghost Chain @SPECIAL_7_9
🎯 100% Free access

Telegram Channel : @APPLE_CRASH_HACK11

🔑 Use Promo Code: SPE91 to unlock premium signals 💥

🚀 Start winning smartly today!

➡️ Send your 9,10 digit ID"""
    
    try:
        bot.send_photo(chat_id, IMAGE_URL, caption=text)
        user_states[chat_id] = 'waiting_for_id'
    except Exception as e:
        bot.send_message(chat_id, text)
        user_states[chat_id] = 'waiting_for_id'

# আইডি ভেরিফাই করার ফাংশন
@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == 'waiting_for_id')
def verify_id(message):
    chat_id = message.chat.id
    user_id_input = message.text.strip()
    
    # চেক করবে আইডিটি ৯ অথবা ১০ ডিজিটের সংখ্যা কি না
    if re.match(r'^\d{9,10}$', user_id_input):
        user_states[chat_id] = 'active'
        
        # বাটন তৈরি করা
        markup = InlineKeyboardMarkup()
        btn_webapp = InlineKeyboardButton("Open Web App", web_app=WebAppInfo(url=WEB_APP_URL))
        btn_signal = InlineKeyboardButton("Message Signal", callback_data="get_signal")
        
        # বাটনগুলো নিচে নিচে অ্যাড করা
        markup.add(btn_webapp)
        markup.add(btn_signal)
        
        bot.send_message(chat_id, "your ID active ✅", reply_markup=markup)
    else:
        bot.send_message(chat_id, "Invalid ID! Please send a valid 9 or 10 digit ID.")

# সিগনাল বাটনের ক্লিক হ্যান্ডলার
@bot.callback_query_handler(func=lambda call: call.data == "get_signal")
def send_signal(call):
    items =['🍎', '🍎', '🍎', '🍎', '🌰']
    random.shuffle(items)
    signal_text = "".join(items)
    
    bot.send_message(call.message.chat.id, f"Here is your signal:\n\n{signal_text}")
    bot.answer_callback_query(call.id)

# বট চালু রাখা
print("Bot is running...")
bot.infinity_polling()
