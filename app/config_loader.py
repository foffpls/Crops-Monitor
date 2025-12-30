"""
Модуль для завантаження конфігурації з змінних оточення.

Всі конфігураційні параметри завантажуються з .env файлу
та доступні через цей модуль.
"""
from dotenv import load_dotenv
import os

# Завантажуємо змінні з .env файлу
load_dotenv()

# Telegram Bot Configuration
BOT_TOKEN = os.getenv("BOT_TOKEN")
"""Токен Telegram бота. Обов'язкова змінна."""

# Exchange Rate Configuration
USD_RATE = float(os.getenv("USD_RATE"))
"""Курс долара для конвертації цін з гривень. Обов'язкова змінна."""

# Admin Configuration
ADMIN_USER_ID = int(os.getenv("ADMIN_USER_ID"))
"""ID адміністратора для отримання запитів на додавання категорій. Обов'язкова змінна."""

# Parser Configuration
MAX_PAGES = int(os.getenv("MAX_PAGES"))
"""Максимальна кількість сторінок для парсингу. Обов'язкова змінна."""

# Optional Configuration
PARSING_URL = os.getenv("PARSING_URL")
"""URL для парсингу"""
