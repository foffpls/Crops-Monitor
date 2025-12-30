import html
import asyncio
from aiogram import Router, types
from aiogram.filters import Command
from app.config_loader import ADMIN_USER_ID
from app.bot.keyboards import build_culture_keyboard, CULTURE_URLS, build_add_key_keyboard
from app.bot.crops_list import crops
from app.bot.parser import fetch_table
from app.bot.analytics import analyze_offers
from app.utils.formatters import format_section, format_comparison, format_admin_message

router = Router()
cache = {}  # кеш для таблиці по культурі
add_key_selections = {}  # зберігає вибрані культури для кожного користувача: {user_id: set(crops)}

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привіт!\n"
                         "/monitor вивести аналітику культур за весь доступний період\n"
                         "/monitor_2025 вивести аналітику культур за 2025 рік\n"
                         "/add_category запропонувати нову категорію культур")

@router.message(Command("monitor"))
async def cmd_monitor(message: types.Message):
    keyboard = build_culture_keyboard()
    await message.answer("Оберіть культуру:", reply_markup=keyboard)

@router.message(Command("monitor_2025"))
async def cmd_monitor_2025(message: types.Message):
    keyboard = build_culture_keyboard(year_filter=2025)
    await message.answer("Оберіть культуру (аналіз за 2025 рік):", reply_markup=keyboard)

@router.message(Command("add_category"))
async def cmd_add_key(message: types.Message):
    """Показує клавіатуру для вибору культур."""
    user_id = message.from_user.id
    
    # Ініціалізуємо порожній набір вибраних культур для користувача
    if user_id not in add_key_selections:
        add_key_selections[user_id] = set()
    
    keyboard = build_add_key_keyboard(add_key_selections[user_id])
    await message.answer("Оберіть культури для додавання:", reply_markup=keyboard)

@router.callback_query(lambda c: c.data and c.data.startswith("culture:"))
async def culture_selected(callback: types.CallbackQuery):
    culture_name = callback.data.split(":", 1)[1]
    await _process_culture_analysis(callback, culture_name, year_filter=None)

@router.callback_query(lambda c: c.data and c.data.startswith("culture_2025:"))
async def culture_selected_2025(callback: types.CallbackQuery):
    culture_name = callback.data.split(":", 1)[1]
    await _process_culture_analysis(callback, culture_name, year_filter=2025)

@router.callback_query(lambda c: c.data and c.data.startswith("add_key_toggle:"))
async def add_key_toggle(callback: types.CallbackQuery):
    """Обробляє натискання на кнопку культури - додає/прибирає галочку."""
    user_id = callback.from_user.id
    crop_idx = int(callback.data.split(":", 1)[1])
    
    # Перевіряємо, чи індекс валідний
    if crop_idx < 0 or crop_idx >= len(crops):
        await callback.answer("❌ Помилка: невалідний індекс культури", show_alert=True)
        return
    
    crop_name = crops[crop_idx]
    
    # Ініціалізуємо набір, якщо його немає
    if user_id not in add_key_selections:
        add_key_selections[user_id] = set()
    
    # Додаємо або прибираємо культуру
    if crop_name in add_key_selections[user_id]:
        add_key_selections[user_id].remove(crop_name)
    else:
        add_key_selections[user_id].add(crop_name)
    
    # Оновлюємо клавіатуру
    keyboard = build_add_key_keyboard(add_key_selections[user_id])
    await callback.message.edit_reply_markup(reply_markup=keyboard)
    await callback.answer()

@router.callback_query(lambda c: c.data == "add_key_done")
async def add_key_done(callback: types.CallbackQuery):
    """Обробляє натискання кнопки 'ГОТОВО' - надсилає запит адміну."""
    user_id = callback.from_user.id
    username = callback.from_user.username or "Невідомий"
    first_name = callback.from_user.first_name or ""
    last_name = callback.from_user.last_name or ""
    full_name = f"{first_name} {last_name}".strip() or username
    
    # Отримуємо вибрані культури
    selected_crops = add_key_selections.get(user_id, set())
    
    # Приховуємо клавіатуру
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.answer()
    
    # Відправляємо повідомлення користувачу
    await callback.message.answer("✅ Запит надіслано")
    
    # Очищаємо вибір користувача
    if user_id in add_key_selections:
        del add_key_selections[user_id]
    
    # Формуємо повідомлення для адміна
    admin_message = format_admin_message(full_name, username, user_id, selected_crops)
    
    # Надсилаємо повідомлення адміну
    try:
        await callback.bot.send_message(ADMIN_USER_ID, admin_message)
    except Exception as e:
        # Якщо не вдалося надіслати адміну, логуємо помилку
        print(f"Помилка надсилання повідомлення адміну: {e}")

@router.callback_query(lambda c: c.data == "cancel")
async def cancel_operation(callback: types.CallbackQuery):
    """Обробляє натискання кнопки 'ВІДМІНИТИ' - видаляє клавіатуру та надсилає повідомлення."""
    user_id = callback.from_user.id
    
    # Очищаємо вибір користувача, якщо він був у процесі додавання категорій
    if user_id in add_key_selections:
        del add_key_selections[user_id]
    
    # Видаляємо клавіатуру
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.answer()
    
    # Надсилаємо повідомлення про скасування
    await callback.message.answer("❌ Операцію скасовано")

async def _process_culture_analysis(callback: types.CallbackQuery, culture_name: str, year_filter: int = None):
    """Загальна функція для обробки аналізу культури з опціональною фільтрацією за роком."""
    # Відповідь на callback, щоб прибрати "loading" на кнопці
    await callback.answer()

    # Замінюємо клавіатуру на проміжне повідомлення
    base_text = f"АНАЛІЗУЮ"
    
    # Смайли для анімації
    animation_emojis = ["⏳", "🔄", "📊", "🔍", "⚙️", "📈", "💫"]
    animation_stop = False
    
    async def animate_loading():
        """Анімація завантаження з прокручуванням смайлів по кожному символу тексту."""
        emoji_index = 0
        position = 0
        forward = True
        text_length = len(base_text)
        
        while not animation_stop:
            emoji = animation_emojis[emoji_index % len(animation_emojis)]
            
            # Вставляємо смайл на позицію position (між символами)
            if position == 0:
                # Смайл на початку
                animated_text = emoji + base_text
            elif position >= text_length:
                # Смайл в кінці
                animated_text = base_text + emoji
            else:
                # Смайл між символами
                animated_text = base_text[:position] + emoji + base_text[position:]
            
            # Змінюємо позицію
            if forward:
                position += 1
                if position > text_length:
                    # Досягли кінця - рухаємось назад
                    forward = False
                    position = text_length
                    emoji_index = (emoji_index + 1) % len(animation_emojis)  # Змінюємо смайл
            else:
                position -= 1
                if position < 0:
                    # Досягли початку - рухаємось вперед
                    forward = True
                    position = 0
                    emoji_index = (emoji_index + 1) % len(animation_emojis)  # Змінюємо смайл
            
            try:
                await callback.message.edit_text(
                    animated_text,
                    reply_markup=None
                )
            except Exception:
                # Якщо повідомлення вже видалено або змінено, зупиняємо анімацію
                break
            
            await asyncio.sleep(0.1)
    
    # Запускаємо анімацію
    animation_task = asyncio.create_task(animate_loading())
    
    try:
        # Завантаження даних
        url = CULTURE_URLS[culture_name]
        cache_key = f"{culture_name}_{year_filter}" if year_filter else culture_name
        if cache_key in cache:
            rows = cache[cache_key]
        else:
            rows = await fetch_table(url)
            cache[cache_key] = rows

        # Аналіз даних з фільтрацією за роком
        analysis = analyze_offers(rows, year_filter=year_filter)
    finally:
        # Зупиняємо анімацію
        animation_stop = True
        animation_task.cancel()
        try:
            await animation_task
        except asyncio.CancelledError:
            pass
    
    # Отримуємо останнє повідомлення для подальшого редагування
    wait_msg = callback.message
    # Надсилаємо три окремі повідомлення
    messages_sent = False
    
    # 1. Повідомлення про "Куплю"
    buy_data = analysis.get("куплю")
    if buy_data:
        buy_text = format_section("куплю", buy_data, culture_name)
        safe_buy_text = html.escape(buy_text)
        buy_chunks = [safe_buy_text[i:i+4000] for i in range(0, len(safe_buy_text), 4000)]
        if buy_chunks:
            await wait_msg.edit_text(buy_chunks[0])
            messages_sent = True
            for chunk in buy_chunks[1:]:
                await callback.message.answer(chunk)
    
    # 2. Повідомлення про "Продам"
    sell_data = analysis.get("продам")
    if sell_data:
        sell_text = format_section("продам", sell_data, culture_name)
        safe_sell_text = html.escape(sell_text)
        sell_chunks = [safe_sell_text[i:i+4000] for i in range(0, len(safe_sell_text), 4000)]
        if sell_chunks:
            if not messages_sent:
                await wait_msg.edit_text(sell_chunks[0])
                messages_sent = True
            else:
                await callback.message.answer(sell_chunks[0])
            for chunk in sell_chunks[1:]:
                await callback.message.answer(chunk)
    
    # 3. Повідомлення про порівняльний аналіз
    if buy_data and sell_data:
        comparison_text = format_comparison(buy_data, sell_data, culture_name)
        safe_comparison_text = html.escape(comparison_text)
        comparison_chunks = [safe_comparison_text[i:i+4000] for i in range(0, len(safe_comparison_text), 4000)]
        if comparison_chunks:
            if not messages_sent:
                await wait_msg.edit_text(comparison_chunks[0])
            else:
                await callback.message.answer(comparison_chunks[0])
            for chunk in comparison_chunks[1:]:
                await callback.message.answer(chunk)
    
    # Якщо немає даних взагалі
    if not buy_data and not sell_data:
        await wait_msg.edit_text("❌ На жаль, дані відсутні для обраної культури.")
