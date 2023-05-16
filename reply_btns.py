from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def start_btn():
    btn = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
    btn.add(KeyboardButton('🎧 All Music'), KeyboardButton('🏆 Top Music'),
            KeyboardButton('🆕 New Music'), KeyboardButton('🎵 Tik-Tok Music'), KeyboardButton('👨🏻‍💻 Admin'))
    return btn


def admin_page():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
    markup.add(KeyboardButton('📊 Statistika'), KeyboardButton('🔔 Reklama'), KeyboardButton('🔙 Back'))
    return markup
