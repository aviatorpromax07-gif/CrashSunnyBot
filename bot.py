import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
import random
import re

# আপনার বটের টোকেন (নিরাপত্তার জন্য এটি পরিবর্তন করে নেওয়াই ভালো)
TOKEN = '8276327075:AAHA-7nrNfRhLCauU90xfuXV3-v2vhiURdE'
bot = telebot.TeleBot(TOKEN)

# অ্যাডমিনদের ইউজারনেম
ADMINS = ['@SPECIAL_7_9', '@SUNNY_BRO1']

# ওয়েব অ্যাপ লিংক এবং ওয়েলকাম ইমেজের লিংক
WEB_APP_URL = 'https://crashsunny.netlify.app/'
# এখানে আপনার ইমেজের লিংকটি দিন
IMAGE_URL = 'https://img.freepik.com/free-vector/welcome-typography-design_1308-115984.jpg' 

# ইউজারদের স্টেট সেভ রাখার ডিকশনারি
user_states = {}

# /start কমান্ড হ্যান্ডলার
@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    text = "Welcome to our Bot!\n\nSend your 9,10 digit ID"
    
    # ইমেজ সহ ওয়েলকাম মেসেজ পাঠানো
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
        # ওয়েব অ্যাপ বাটন
        btn_webapp = InlineKeyboardButton("Open Web App", web_app=WebAppInfo(url=WEB_APP_URL))
        # সিগনাল বাটন
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
    # ৫টি ইমেজের লিস্ট (৪টি আপেল, ১টি অন্য কিছু)
    items =['🍎', '🍎', '🍎', '🍎', '🌰']
    
    # র্যান্ডমলি শাফল (এলোমেলো) করা
    random.shuffle(items)
    
    # লিস্টটিকে স্ট্রিংয়ে রূপান্তর করা
    signal_text = "".join(items)
    
    # সিগনাল মেসেজটি ইউজারের কাছে পাঠানো
    bot.send_message(call.message.chat.id, f"Here is your signal:\n\n{signal_text}")
    
    # লোডিং অ্যানিমেশন বন্ধ করা
    bot.answer_callback_query(call.id)

# বট চালু রাখা
print("Bot is running...")
bot.infinity_polling()
