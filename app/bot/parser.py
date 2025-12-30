"""
Модуль для парсингу даних з сайту Graintrade.com.ua.

Відповідає за отримання та обробку оголошень про купівлю/продаж
зернових культур з веб-сайту.
"""
import aiohttp
from bs4 import BeautifulSoup
import re
from app.config_loader import USD_RATE, MAX_PAGES


async def fetch_table(url: str) -> list[dict]:
    """
    Парсить таблицю оголошень з сайту Graintrade.com.ua.
    
    Args:
        url: URL сторінки з оголошеннями для парсингу
        
    Returns:
        Список словників з даними оголошень. Кожен словник містить:
        - date: Дата оголошення (рядок)
        - type: Тип оголошення ('куплю' або 'продам')
        - price: Ціна в USD за 1 тонну (ціле число)
        
    Note:
        Функція парсить до MAX_PAGES сторінок. Ціни автоматично
        конвертуються з гривень у долари за курсом USD_RATE.
    """
    offers = []
    async with aiohttp.ClientSession() as session:
        for page in range(1, MAX_PAGES + 1):
            # Визначаємо, чи в URL вже є параметри
            separator = "&" if "?" in url else "?"
            page_url = f"{url}{separator}Ad_page={page}"
            try:
                async with session.get(page_url) as resp:
                    text = await resp.text()
                    soup = BeautifulSoup(text, 'html.parser')
                    
                    # Знаходимо таблицю з оголошеннями (шукаємо tbody з рядками)
                    tbody = soup.find('tbody')
                    if not tbody:
                        continue
                    
                    rows = tbody.find_all('tr')
                    
                    for r in rows:
                        try:
                            cells = r.find_all('td')
                            if len(cells) < 6:
                                continue
                            
                            # Отримуємо дату (перша колонка)
                            date_elem = cells[0]
                            date = date_elem.get_text(strip=True) if date_elem else ''
                            
                            # Отримуємо тип оголошення (третя колонка, span)
                            type_elem = cells[2].find('span') if len(cells) > 2 else None
                            type_offer = type_elem.get_text(strip=True).lower() if type_elem else ''
                            
                            # Отримуємо ціну (шоста колонка)
                            price_elem = cells[5] if len(cells) > 5 else None
                            price_text = price_elem.get_text(strip=True) if price_elem else ''
                            
                            # Парсимо ціну: прибираємо все, крім цифр, крапки або коми
                            price_clean = re.sub(r"[^\d.,]", "", price_text).replace(",", ".")
                            if not price_clean:
                                continue
                            
                            try:
                                price_value = float(price_clean)
                                if price_value <= 0:
                                    continue
                                
                                # Конвертація в USD, якщо гривні
                                if "грн" in price_text.lower():
                                    price_value = price_value / USD_RATE
                                

                                price = int(round(price_value))
                                
                                if price <= 0:
                                    continue
                            except (ValueError, TypeError):
                                continue
                            
                            offers.append({
                                "date": date,
                                "type": type_offer,
                                "price": price
                            })
                        except (IndexError, AttributeError, ValueError, TypeError):
                            continue
            except Exception:
                continue  # Пропускаємо сторінку при помилці
    
    return offers
