"""
Точка входу для Telegram бота Graintrade Monitor.

Запускає бота та налаштовує обробку подій.
"""
import asyncio
from aiogram import Bot, Dispatcher
from app.config_loader import BOT_TOKEN
from app.bot.handlers import router


async def main():
    """
    Головна функція для запуску бота.
    
    Створює екземпляри Bot та Dispatcher, підключає роутер
    та запускає polling для обробки повідомлень.
    """
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # Підключаємо роутер з обробниками
    dp.include_router(router)

    try:
        print("🤖 Бот Graintrade Monitor запущено...")
        await dp.start_polling(bot)
    except KeyboardInterrupt:
        print("\n⚠️ Бот зупинено користувачем")
    except Exception as e:
        print(f"❌ Помилка при роботі бота: {e}")
    finally:
        await bot.session.close()
        print("✅ Сесія бота закрита")


if __name__ == "__main__":
    asyncio.run(main())
