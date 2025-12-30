from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from app.bot.crops_list import crops

CULTURE_URLS = {
    "Кукурудза": "https://graintrade.com.ua/birzha/kuplyu-ta-prodam-kukurudzu-v-ukraini-f8",
    "Соя": "https://graintrade.com.ua/birzha/kuplyu-ta-prodam-soyu-po-vsij-ukraini-f4",
    "Соя без ГМО": "https://graintrade.com.ua/birzha?Ad[countries_id]=&Ad[area_id]=&Ad[terminal_id]=&Ad[incoterms]=&Ad[currency]=&Ad[market_selector]=&Ad[user_id]=&Ad[customs_id]=&Ad[expired]=show&Ad[price_max]=&Ad[price_min]=&Ad[pdv]=&Ad[date_max]=&Ad[date_min]=&Ad[size_max]=&Ad[size_min]=&Ad[culture]=156&Ad[type]=7&Ad[elevator_id]=&Ad[target_processor_id]=",
    "Соняшник": "https://graintrade.com.ua/birzha/kuplyu-ta-prodam-sonyashnik-v-ukraini-f2",
    "Олія соняшникова": "https://graintrade.com.ua/birzha/kuplyu-oliyu-sonyashnikovu-prodam-oliyu-sonyashnikov-v-ukraini-f22",
    "Пшениця 1 клас": "https://graintrade.com.ua/birzha?Ad[countries_id]=&Ad[area_id]=&Ad[terminal_id]=&Ad[incoterms]=&Ad[currency]=&Ad[market_selector]=&Ad[user_id]=&Ad[customs_id]=&Ad[expired]=show&Ad[price_max]=&Ad[price_min]=&Ad[pdv]=&Ad[date_max]=&Ad[date_min]=&Ad[size_max]=&Ad[size_min]=&Ad[culture]=95&Ad[type]=7&Ad[elevator_id]=&Ad[target_processor_id]=",
    "Пшениця 2 клас": "https://graintrade.com.ua/birzha/kuplyu-ta-prodam-pshenitcyu-v-ukraini-f9",
    "Пшениця 3 клас": "https://graintrade.com.ua/birzha?Ad[countries_id]=&Ad[area_id]=&Ad[terminal_id]=&Ad[incoterms]=&Ad[currency]=&Ad[market_selector]=&Ad[user_id]=&Ad[customs_id]=&Ad[expired]=show&Ad[price_max]=&Ad[price_min]=&Ad[pdv]=&Ad[date_max]=&Ad[date_min]=&Ad[size_max]=&Ad[size_min]=&Ad[culture]=88&Ad[type]=7&Ad[elevator_id]=&Ad[target_processor_id]=",
    "Пшениця 4 клас": "https://graintrade.com.ua/birzha?Ad[countries_id]=&Ad[area_id]=&Ad[terminal_id]=&Ad[incoterms]=&Ad[currency]=&Ad[market_selector]=&Ad[user_id]=&Ad[customs_id]=&Ad[expired]=show&Ad[price_max]=&Ad[price_min]=&Ad[pdv]=&Ad[date_max]=&Ad[date_min]=&Ad[size_max]=&Ad[size_min]=&Ad[culture]=108&Ad[type]=7&Ad[elevator_id]=&Ad[target_processor_id]=",
    "Пшениця 5 клас": "https://graintrade.com.ua/birzha?Ad[countries_id]=&Ad[area_id]=&Ad[terminal_id]=&Ad[incoterms]=&Ad[currency]=&Ad[market_selector]=&Ad[user_id]=&Ad[customs_id]=&Ad[expired]=show&Ad[price_max]=&Ad[price_min]=&Ad[pdv]=&Ad[date_max]=&Ad[date_min]=&Ad[size_max]=&Ad[size_min]=&Ad[culture]=89&Ad[type]=7&Ad[elevator_id]=&Ad[target_processor_id]=",
    "Пшениця 6 клас": "https://graintrade.com.ua/birzha?Ad[countries_id]=&Ad[area_id]=&Ad[terminal_id]=&Ad[incoterms]=&Ad[currency]=&Ad[market_selector]=&Ad[user_id]=&Ad[customs_id]=&Ad[expired]=show&Ad[price_max]=&Ad[price_min]=&Ad[pdv]=&Ad[date_max]=&Ad[date_min]=&Ad[size_max]=&Ad[size_min]=&Ad[culture]=90&Ad[type]=7&Ad[elevator_id]=&Ad[target_processor_id]=",
    "Пшениця Тверда": "https://graintrade.com.ua/birzha?Ad[countries_id]=&Ad[area_id]=&Ad[terminal_id]=&Ad[incoterms]=&Ad[currency]=&Ad[market_selector]=&Ad[user_id]=&Ad[customs_id]=&Ad[expired]=show&Ad[price_max]=&Ad[price_min]=&Ad[pdv]=&Ad[date_max]=&Ad[date_min]=&Ad[size_max]=&Ad[size_min]=&Ad[culture]=171&Ad[type]=7&Ad[elevator_id]=&Ad[target_processor_id]=",
    "Ріпак 1кл до 35мкм без ГМО": "https://graintrade.com.ua/birzha?Ad[countries_id]=&Ad[area_id]=&Ad[terminal_id]=&Ad[incoterms]=&Ad[currency]=&Ad[market_selector]=&Ad[user_id]=&Ad[customs_id]=&Ad[expired]=show&Ad[price_max]=&Ad[price_min]=&Ad[pdv]=&Ad[date_max]=&Ad[date_min]=&Ad[size_max]=&Ad[size_min]=&Ad[culture]=148&Ad[type]=7&Ad[elevator_id]=&Ad[target_processor_id]=",
    "Ріпак 2кл від 35мкм без ГМО": "https://graintrade.com.ua/birzha?Ad[countries_id]=&Ad[area_id]=&Ad[terminal_id]=&Ad[incoterms]=&Ad[currency]=&Ad[market_selector]=&Ad[user_id]=&Ad[customs_id]=&Ad[expired]=show&Ad[price_max]=&Ad[price_min]=&Ad[pdv]=&Ad[date_max]=&Ad[date_min]=&Ad[size_max]=&Ad[size_min]=&Ad[culture]=149&Ad[type]=7&Ad[elevator_id]=&Ad[target_processor_id]=",
    "Ріпак в/г до 25мкм без ГМО": "https://graintrade.com.ua/birzha?Ad[countries_id]=&Ad[area_id]=&Ad[terminal_id]=&Ad[incoterms]=&Ad[currency]=&Ad[market_selector]=&Ad[user_id]=&Ad[customs_id]=&Ad[expired]=show&Ad[price_max]=&Ad[price_min]=&Ad[pdv]=&Ad[date_max]=&Ad[date_min]=&Ad[size_max]=&Ad[size_min]=&Ad[culture]=77&Ad[type]=7&Ad[elevator_id]=&Ad[target_processor_id]=",
    "Ріпак з ГМО": "https://graintrade.com.ua/birzha?Ad[countries_id]=&Ad[area_id]=&Ad[terminal_id]=&Ad[incoterms]=&Ad[currency]=&Ad[market_selector]=&Ad[user_id]=&Ad[customs_id]=&Ad[expired]=show&Ad[price_max]=&Ad[price_min]=&Ad[pdv]=&Ad[date_max]=&Ad[date_min]=&Ad[size_max]=&Ad[size_min]=&Ad[culture]=137&Ad[type]=7&Ad[elevator_id]=&Ad[target_processor_id]=",
    "Ячмінь": "https://graintrade.com.ua/birzha/kuplyu-ta-prodam-yachmin-v-ukraini-f10"
}


def build_culture_keyboard(year_filter: int = None) -> InlineKeyboardMarkup:
    """
    Будує клавіатуру для вибору культури.
    
    Args:
        year_filter: Якщо вказано (наприклад, 2025), callback_data буде містити префікс culture_2025:
    """
    # будуємо список рядків (по 2 кнопки в рядок)
    keyboard_rows = []
    row = []
    prefix = f"culture_{year_filter}:" if year_filter else "culture:"
    for i, name in enumerate(CULTURE_URLS):
        btn = InlineKeyboardButton(text=name, callback_data=f"{prefix}{name}")
        row.append(btn)
        if (i + 1) % 2 == 0:
            keyboard_rows.append(row)
            row = []
    if row:
        keyboard_rows.append(row)
    
    # Додаємо кнопку "ВІДМІНИТИ"
    keyboard_rows.append([InlineKeyboardButton(text="❌ ВІДМІНИТИ", callback_data="cancel")])

    return InlineKeyboardMarkup(inline_keyboard=keyboard_rows)


def build_add_key_keyboard(selected_crops: set[str]) -> InlineKeyboardMarkup:
    """
    Будує клавіатуру для вибору культур з можливістю відмітки галочками.
    
    Args:
        selected_crops: Множина вибраних культур (з галочками)
    """
    keyboard_rows = []
    row = []
    
    for idx, crop in enumerate(crops):
        # Додаємо галочку, якщо культура вибрана
        text = f"✅ {crop}" if crop in selected_crops else crop
        # Використовуємо індекс замість повної назви для callback_data (обмеження Telegram - 64 символи)
        btn = InlineKeyboardButton(text=text, callback_data=f"add_key_toggle:{idx}")
        row.append(btn)
        # По 2 кнопки в рядок
        if len(row) == 2:
            keyboard_rows.append(row)
            row = []
    
    # Додаємо останній рядок, якщо є залишок
    if row:
        keyboard_rows.append(row)
    
    # Додаємо кнопки "ГОТОВО" та "ВІДМІНИТИ"
    keyboard_rows.append([
        InlineKeyboardButton(text="✅ ГОТОВО", callback_data="add_key_done"),
        InlineKeyboardButton(text="❌ ВІДМІНИТИ", callback_data="cancel")
    ])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard_rows)
