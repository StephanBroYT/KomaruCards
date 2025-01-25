import sqlite3
import json

def setup_database():
    conn = sqlite3.connect("komaru.db")
    c = conn.cursor()
    
    # Создаем таблицу пользователей
    c.execute(
        """CREATE TABLE IF NOT EXISTS users
            (user_id INTEGER PRIMARY KEY,
            money INTEGER)"""
    )
    
    # Создаем таблицу для хранения карточек пользователей с уникальным индексом
    c.execute(
        """CREATE TABLE IF NOT EXISTS user_cards
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            card_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            UNIQUE(user_id, card_id))"""
    )
    
    conn.commit()
    conn.close()

setup_database()

def add_card_to_user(user_id: int, card_id: int) -> bool:
    """Добавляет карточку пользователю"""
    try:
        conn = sqlite3.connect("komaru.db")
        c = conn.cursor()
        
        money = get_card_by_id(card_id).get("money", 0)
        # Проверяем существует ли пользователь
        c.execute("INSERT OR IGNORE INTO users (user_id, money) VALUES (?, ?)", (user_id, money))
        
        # Добавляем карточку, игнорируем если уже существует
        c.execute("INSERT OR IGNORE INTO user_cards (user_id, card_id) VALUES (?, ?)", 
                 (user_id, card_id))
        
        # Добавляем деньги в любом случае
        c.execute("UPDATE users SET money = money + ? WHERE user_id = ?", (money, user_id))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error adding card: {e}")
        return False

def get_user_cards(user_id: int) -> list:
    """Возвращает список ID карточек пользователя"""
    try:
        with sqlite3.connect("komaru.db") as conn:
            c = conn.cursor()
            c.execute("SELECT card_id FROM user_cards WHERE user_id = ?", (user_id,))
            return [card[0] for card in c.fetchall()]
    except Exception as e:
        print(f"Ошибка при получении карточек: {e}")
        return []

def get_user_money(user_id: int) -> list:
    """Возвращает список ID карточек пользователя"""
    try:
        with sqlite3.connect("komaru.db") as conn:
            c = conn.cursor()
            c.execute("SELECT money FROM users WHERE user_id = ?", (user_id,))
            return [card[0] for card in c.fetchall()]
    except Exception as e:
        print(f"Ошибка при получении монет: {e}")
        return []

def get_users_id() -> list:
    """Возвращает список ID пользователей"""
    try:
        with sqlite3.connect("komaru.db") as conn:
            c = conn.cursor()
            c.execute("SELECT user_id FROM users")
            return [card[0] for card in c.fetchall()]
    except Exception as e:
        print(f"Ошибка при получении ids: {e}")
        return []
    
def get_cards() -> list:
    """Возвращает список всех карточек"""
    try:
        with open("komars.json", "r", encoding="UTF-8") as file:
            cards = json.loads(file.read())
            return cards
    except Exception as e:
        print(f"Ошибка при получении карточек: {e}")
        return {}

def get_card_by_id(card_id: str) -> dict:
    """Возвращает информацию о карточке по её ID из JSON файла"""
    try:
        with open("komars.json", "r", encoding="UTF-8") as file:
            cards = json.loads(file.read())
            return cards.get(str(card_id), {})
    except Exception as e:
        print(f"Ошибка при получении карточки: {e}")
        return {}