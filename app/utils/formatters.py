"""
Модуль для форматування тексту аналітики та повідомлень.

Містить функції для створення читабельних текстових звітів
на основі аналітичних даних та формування повідомлень для адміністратора.
"""
from datetime import datetime


def format_section(offer_type: str, data: dict, culture_name: str) -> str:
    """
    Формує текстовий звіт для одного типу оголошень (куплю/продам).
    
    Args:
        offer_type: Тип оголошень ('куплю' або 'продам')
        data: Словник з аналітичними даними
        culture_name: Назва культури для відображення
        
    Returns:
        Відформатований текст звіту
    """
    if not data:
        return f"❌ {offer_type.capitalize()}: На жаль, дані відсутні\nЦе означає, що за обраний період не знайдено жодних оголошень цього типу."
    
    text_parts = [
        f"📋 РОЗДІЛ: {offer_type.upper()}",
        f"{'='*33}",
        f"📊 Аналітика по {culture_name}",
        ""
    ]
    
    # Загальна інформація з поясненнями
    text_parts.append(f"📅 ПЕРІОД АНАЛІЗУ:")
    text_parts.append(f"   З {data.get('first_date', '-')} по {data.get('last_date', '-')}")
    
    text_parts.append(f"\n📊 АКТИВНІСТЬ НА РИНКУ:")
    text_parts.append(f"   • Сьогодні: {data.get('count_today', 0)} оголошень")
    text_parts.append(f"   • За останні 3 дні: {data.get('count_last_3', 0)} оголошень")
    text_parts.append(f"   • За останні 7 днів: {data.get('count_last_7', 0)} оголошень")
    text_parts.append(f"   • Всього за період: {data.get('count_total', 0)} оголошень")
    
    # Статистика цін з детальними поясненнями
    text_parts.append(f"\n💰 СТАТИСТИКА ЦІН (USD за 1 тонну):")
    text_parts.append(f"   • Середня ціна: {data.get('avg_price', 0)} USD")
    text_parts.append(f"   • Медіана: {data.get('median_price', 0)} USD")
    if data.get('avg_price') and data.get('median_price'):
        diff = abs(data.get('avg_price', 0) - data.get('median_price', 0))
        if diff > 50:
            text_parts.append(f"     ⚠️ Велика різниця між середньою та медіаною ({diff} USD)")
            text_parts.append(f"       вказує на значні коливання цін на ринку")
    
    text_parts.append(f"   • Максимальна ціна: {data.get('max_price', 0)} USD ({data.get('max_price_date', '-')})")
    text_parts.append(f"   • Мінімальна ціна: {data.get('min_price', 0)} USD ({data.get('min_price_date', '-')})")
    
    price_range = data.get('max_price', 0) - data.get('min_price', 0)
    if price_range > 0:
        text_parts.append(f"   • Діапазон коливань: {price_range} USD")
        if price_range > 200:
            text_parts.append(f"     ⚠️ Великий діапазон вказує на високу волатильність ринку")
    
    text_parts.append(f"   • Стандартне відхилення: {data.get('std_dev', 0)} USD")
    text_parts.append(f"     ↳ Показує наскільки розсіяні ціни відносно середньої")
    if data.get('std_dev', 0) > 100:
        text_parts.append(f"     ⚠️ Високе відхилення означає значні коливання цін")
    elif data.get('std_dev', 0) < 30:
        text_parts.append(f"     ✓ Низьке відхилення вказує на стабільність цін")
    
    # Динаміка цін з інтерпретацією
    text_parts.append(f"\n📈 ДИНАМІКА ЦІН ЗА ПЕРІОДИ:")
    if data.get('avg_price_today'):
        text_parts.append(f"   • Сьогодні: {data.get('avg_price_today', 0)} USD")
    if data.get('avg_price_last_3'):
        text_parts.append(f"   • За останні 3 дні: {data.get('avg_price_last_3', 0)} USD")
    if data.get('avg_price_last_7'):
        text_parts.append(f"   • За останні 7 днів: {data.get('avg_price_last_7', 0)} USD")
    
    # Порівняння динаміки
    if data.get('avg_price_today') and data.get('avg_price_last_7'):
        today_price = data.get('avg_price_today', 0)
        week_price = data.get('avg_price_last_7', 0)
        if today_price > 0 and week_price > 0:
            week_change = ((today_price - week_price) / week_price) * 100
            if abs(week_change) > 5:
                if week_change > 0:
                    text_parts.append(f"     📈 Ціна сьогодні вища за тижневу на {abs(week_change):.1f}%")
                else:
                    text_parts.append(f"     📉 Ціна сьогодні нижча за тижневу на {abs(week_change):.1f}%")
    
    # Тренд з детальним описом
    trend_emoji = "📈" if "ЗРОСТАЄ" in data.get('trend', '') else ("📉" if "СПАДАЄ" in data.get('trend', '') else "➡️")
    text_parts.append(f"\n{trend_emoji} ЗАГАЛЬНИЙ ТРЕНД:")
    text_parts.append(f"   {data.get('trend', '-')}")
    if data.get('price_change_percent'):
        change_sign = "+" if data.get('price_change_percent', 0) > 0 else ""
        change_val = data.get('price_change_percent', 0)
        text_parts.append(f"   • Зміна від початку періоду: {change_sign}{change_val}%")
        text_parts.append(f"     ↳ Показує загальну зміну ціни від першої до останньої дати")
        if abs(change_val) > 10:
            text_parts.append(f"     ⚠️ Значна зміна ціни за період аналізу")
        elif abs(change_val) < 2:
            text_parts.append(f"     ✓ Стабільна ціна протягом періоду")
    
    # Динаміка за останні 7 днів з інтерпретацією
    daily_avg = data.get('daily_avg', {})
    if daily_avg:
        text_parts.append(f"\n📆 ДЕННА ДИНАМІКА (останні 7 днів):")
        text_parts.append(f"   Детальний розподіл середніх цін по днях:")
        sorted_days = sorted(daily_avg.items(), key=lambda x: datetime.strptime(x[0], "%d.%m.%Y"))
        for day, price in sorted_days[-7:]:
            text_parts.append(f"   • {day}: {price} USD")
        
        # Аналіз тренду за останні дні
        if len(sorted_days) >= 3:
            recent_prices = [p for _, p in sorted_days[-3:]]
            if len(recent_prices) == 3:
                if recent_prices[2] > recent_prices[0]:
                    text_parts.append(f"   📈 За останні 3 дні ціна зросла на {recent_prices[2] - recent_prices[0]} USD")
                elif recent_prices[2] < recent_prices[0]:
                    text_parts.append(f"   📉 За останні 3 дні ціна впала на {recent_prices[0] - recent_prices[2]} USD")
                else:
                    text_parts.append(f"   ➡️ Ціна залишається стабільною")
    
    return '\n'.join(text_parts)


def format_comparison(buy_data: dict, sell_data: dict, culture_name: str) -> str:
    """
    Формує текстовий звіт порівняльного аналізу між покупцями та продавцями.
    
    Args:
        buy_data: Словник з аналітичними даними для типу 'куплю'
        sell_data: Словник з аналітичними даними для типу 'продам'
        culture_name: Назва культури для відображення
        
    Returns:
        Відформатований текст порівняльного аналізу
    """
    text_parts = [
        f"⚖️ КУПЛЮ vs ПРОДАМ",
        f"{'='*33}",
        f"📊 Аналітика по {culture_name}",
        "",
        "Цей розділ дозволяє порівняти ринкові умови між покупцями та продавцями."
    ]
    
    price_diff = buy_data.get('avg_price', 0) - sell_data.get('avg_price', 0)
    text_parts.append(f"\n💰 ПОРІВНЯННЯ ЦІН:")
    if price_diff > 0:
        text_parts.append(f"   • Середня ціна Куплю: {buy_data.get('avg_price', 0)} USD")
        text_parts.append(f"   • Середня ціна Продам: {sell_data.get('avg_price', 0)} USD")
        text_parts.append(f"   • Різниця: Куплю вище на {abs(price_diff)} USD ({abs(price_diff)/sell_data.get('avg_price', 1)*100:.1f}%)")
        text_parts.append(f"     ↳ Це означає, що покупці готові платити більше, ніж просять продавці")
        text_parts.append(f"     💡 Висновок: Ринок сприятливий для продавців")
    elif price_diff < 0:
        text_parts.append(f"   • Середня ціна Куплю: {buy_data.get('avg_price', 0)} USD")
        text_parts.append(f"   • Середня ціна Продам: {sell_data.get('avg_price', 0)} USD")
        text_parts.append(f"   • Різниця: Продам вище на {abs(price_diff)} USD ({abs(price_diff)/buy_data.get('avg_price', 1)*100:.1f}%)")
        text_parts.append(f"     ↳ Це означає, що продавці просять більше, ніж готові платити покупці")
        text_parts.append(f"     💡 Висновок: Ринок сприятливий для покупців")
    else:
        text_parts.append(f"   • Середні ціни практично однакові")
        text_parts.append(f"   • Куплю: {buy_data.get('avg_price', 0)} USD")
        text_parts.append(f"   • Продам: {sell_data.get('avg_price', 0)} USD")
        text_parts.append(f"     ↳ Це вказує на збалансований ринок")
        text_parts.append(f"     💡 Висновок: Ринок збалансований, умови справедливі")
    
    count_diff = buy_data.get('count_total', 0) - sell_data.get('count_total', 0)
    text_parts.append(f"\n📊 ПОРІВНЯННЯ АКТИВНОСТІ:")
    text_parts.append(f"   • Оголошень Куплю: {buy_data.get('count_total', 0)}")
    text_parts.append(f"   • Оголошень Продам: {sell_data.get('count_total', 0)}")
    if count_diff > 0:
        text_parts.append(f"   • Більше оголошень Куплю на {abs(count_diff)} (+{abs(count_diff)/sell_data.get('count_total', 1)*100:.1f}%)")
        text_parts.append(f"     ↳ Висока активність покупців на ринку")
        text_parts.append(f"     💡 Висновок: Попит перевищує пропозицію")
    elif count_diff < 0:
        text_parts.append(f"   • Більше оголошень Продам на {abs(count_diff)} (+{abs(count_diff)/buy_data.get('count_total', 1)*100:.1f}%)")
        text_parts.append(f"     ↳ Висока активність продавців на ринку")
        text_parts.append(f"     💡 Висновок: Пропозиція перевищує попит")
    else:
        text_parts.append(f"   • Кількість оголошень однакова")
        text_parts.append(f"     ↳ Збалансована активність на ринку")
    
    text_parts.append(f"\n{'='*33}")
    text_parts.append(f"📌 ПРИМІТКА:")
    text_parts.append(f"• Всі дані базуються на аналізі оголошень з біржі Graintrade")
    text_parts.append(f"• Ціни вказані в доларах США за 1 тонну")
    text_parts.append(f"• Рекомендується регулярно перевіряти оновлення")
    text_parts.append(f"• При прийнятті рішень враховуйте також інші фактори ринку")
    
    return '\n'.join(text_parts)


def format_admin_message(full_name: str, username: str, user_id: int, selected_crops: set[str]) -> str:
    """
    Формує повідомлення для адміністратора про запит на додавання культур.
    
    Args:
        full_name: Повне ім'я користувача
        username: Username користувача
        user_id: ID користувача
        selected_crops: Множина вибраних культур
        
    Returns:
        Відформатоване повідомлення для адміністратора
    """
    if selected_crops:
        crops_list = "\n".join(f"• {crop}" for crop in sorted(selected_crops))
        admin_message = (
            f"📋 Новий запит на додавання культур\n\n"
            f"👤 Користувач: {full_name} (@{username})\n"
            f"🆔 ID: {user_id}\n"
            f"🕐 Час: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n\n"
            f"🌾 Запрошені культури ({len(selected_crops)}):\n{crops_list}"
        )
    else:
        admin_message = (
            f"📋 Запит на додавання культур (без вибору)\n\n"
            f"👤 Користувач: {full_name} (@{username})\n"
            f"🆔 ID: {user_id}\n"
            f"🕐 Час: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n\n"
            f"⚠️ Користувач не вибрав жодної культури"
        )
    
    return admin_message

