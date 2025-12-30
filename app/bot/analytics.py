"""
Модуль для аналізу даних про оголошення зернових культур.

Відповідає за обчислення статистики, трендів та динаміки цін
на основі отриманих даних з парсера.
"""
from datetime import datetime, date, timedelta
import re
import statistics
from app.config_loader import USD_RATE


def parse_price(price_value) -> int | None:
    """
    Парсить ціну з рядка або числа та переводить у USD за 1т.
    
    Args:
        price_value: Ціна у вигляді рядка (з валютою) або числа
        
    Returns:
        Ціна в USD за 1 тонну як ціле число, або None якщо парсинг не вдався
        
    Note:
        Якщо в рядку вказано "грн", ціна автоматично конвертується
        у долари за курсом USD_RATE.
    """
    if price_value is None:
        return None

    # Якщо це вже число, просто конвертуємо в int
    if isinstance(price_value, (float, int)):
        return int(round(price_value))

    # Якщо це рядок, парсимо його
    price_str = str(price_value)
    price_clean = re.sub(r"[^\d.,]", "", price_str).replace(",", ".")
    
    if not price_clean:
        return None
    
    try:
        price_value = float(price_clean)
        # Конвертація в USD, якщо гривні
        if "грн" in price_str.lower():
            price_value /= USD_RATE
        return int(round(price_value))
    except (ValueError, TypeError):
        return None


def analyze_offers(rows: list[dict], year_filter: int = None) -> dict:
    """
    Аналізує оголошення для однієї культури та обчислює статистику.
    
    Args:
        rows: Список оголошень з полями: 'date', 'type', 'price'
        year_filter: Опціональний рік для фільтрації (наприклад, 2025)
        
    Returns:
        Словник з аналітикою для типу 'куплю' та 'продам'. Кожен розділ містить:
        - count_today: Кількість оголошень сьогодні
        - count_total: Загальна кількість оголошень
        - first_date, last_date: Перша та остання дати
        - avg_price, median_price: Середня та медіанна ціна
        - max_price, min_price: Максимальна та мінімальна ціна
        - std_dev: Стандартне відхилення
        - avg_price_today, avg_price_last_3, avg_price_last_7: Середні ціни за періоди
        - price_change_percent: Відсоток зміни ціни
        - trend: Тренд (зростає/падає/немає змін)
        - daily_avg: Словник середніх цін по днях за останні 7 днів
        
    Note:
        Ціни очікуються в USD за 1 тонну. Фільтрація за роком
        застосовується до дат оголошень.
    """
    analysis = {"куплю": {}, "продам": {}}

    for offer_type in ["куплю", "продам"]:
        filtered = [r for r in rows if r.get('type') == offer_type]
        if not filtered:
            analysis[offer_type] = None
            continue

        valid_rows = []
        for r in filtered:
            # Дата
            try:
                date_part = str(r.get('date', '')).split()[0]
                r_date = datetime.strptime(date_part, "%d.%m.%Y").date()
                
                # Фільтрація за роком, якщо вказано
                if year_filter is not None and r_date.year != year_filter:
                    continue
            except (ValueError, TypeError):
                continue

            # Ціна у USD
            price_value = parse_price(r.get("price", ""))
            if price_value is None:
                continue

            valid_rows.append({
                "date": r_date,
                "price": price_value
            })

        if not valid_rows:
            analysis[offer_type] = None
            continue

        # Сортуємо за датою для правильного аналізу
        valid_rows.sort(key=lambda x: x["date"])
        
        dates = [r["date"] for r in valid_rows]
        prices = [r["price"] for r in valid_rows if r["price"] > 0]
        prices_with_dates = [(r["date"], r["price"]) for r in valid_rows if r["price"] > 0]

        today = date.today()
        count_today = sum(1 for r in valid_rows if r["date"] == today)
        count_total = len(valid_rows)
        first_date = min(dates)
        last_date = max(dates)
        
        # Базова статистика цін (враховуємо всі оголошення)
        avg_price = int(round(sum(prices) / len(prices))) if prices else 0
        max_price = max(prices) if prices else 0
        min_price = min(prices) if prices else 0
        
        # Медіана та стандартне відхилення
        median_price = int(round(statistics.median(prices))) if len(prices) > 0 else 0
        std_dev = int(round(statistics.stdev(prices))) if len(prices) > 1 else 0
        
        # Найвища та найнижча ціна з датами
        max_price_date = None
        min_price_date = None
        if prices_with_dates:
            max_price_date = max(prices_with_dates, key=lambda x: x[1])[0].strftime("%d.%m.%Y")
            min_price_date = min(prices_with_dates, key=lambda x: x[1])[0].strftime("%d.%m.%Y")
        
        # Статистика за останні дні
        last_3_days = today - timedelta(days=3)
        last_7_days = today - timedelta(days=7)
        
        prices_last_3 = [r["price"] for r in valid_rows if r["date"] >= last_3_days and r["price"] > 0]
        prices_last_7 = [r["price"] for r in valid_rows if r["date"] >= last_7_days and r["price"] > 0]
        
        avg_price_last_3 = int(round(sum(prices_last_3) / len(prices_last_3))) if prices_last_3 else 0
        avg_price_last_7 = int(round(sum(prices_last_7) / len(prices_last_7))) if prices_last_7 else 0
        count_last_3 = len([r for r in valid_rows if r["date"] >= last_3_days])
        count_last_7 = len([r for r in valid_rows if r["date"] >= last_7_days])
        
        # Середня ціна сьогодні
        prices_today = [r["price"] for r in valid_rows if r["date"] == today and r["price"] > 0]
        avg_price_today = int(round(sum(prices_today) / len(prices_today))) if prices_today else 0
        
        # Зміна ціни та тренд
        price_change_percent = 0
        trend = "немає змін"
        if prices and len(prices) >= 2:
            price_change_percent = round(((prices[-1] - prices[0]) / prices[0]) * 100, 2) if prices[0] else 0
            trend = "зростає ↑" if price_change_percent > 0 else (
                "падає ↓" if price_change_percent < 0 else "немає змін")
        
        # Динаміка за останні 7 днів (середня ціна по днях)
        daily_prices = {}
        for r in valid_rows:
            if r["date"] >= last_7_days:
                day_str = r["date"].strftime("%d.%m.%Y")
                if day_str not in daily_prices:
                    daily_prices[day_str] = []
                daily_prices[day_str].append(r["price"])
        
        daily_avg = {day: int(round(sum(p) / len(p))) for day, p in daily_prices.items() if p}

        analysis[offer_type] = {
            "count_today": count_today,
            "count_total": count_total,
            "first_date": first_date.strftime("%d.%m.%Y"),
            "last_date": last_date.strftime("%d.%m.%Y"),
            "avg_price": avg_price,
            "median_price": median_price,
            "std_dev": std_dev,
            "max_price": max_price,
            "max_price_date": max_price_date,
            "min_price": min_price,
            "min_price_date": min_price_date,
            "avg_price_today": avg_price_today,
            "avg_price_last_3": avg_price_last_3,
            "avg_price_last_7": avg_price_last_7,
            "count_last_3": count_last_3,
            "count_last_7": count_last_7,
            "price_change_percent": price_change_percent,
            "trend": trend,
            "daily_avg": daily_avg
        }

    return analysis
 