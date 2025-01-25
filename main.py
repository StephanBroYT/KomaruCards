ME_ID = 1127025574
import telebot, methods, logging

komars = ["комар", "комару", "komap", "komaru"]
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(message)s",
    datefmt="%d/%m/%Y %I:%M:%S %p",
    handlers=[
        logging.FileHandler("./logs.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)

bot = telebot.TeleBot("7856679795:AAELjKK6_1461_0lzSp8eglvoXVFDBAWRDs")


@bot.message_handler(commands=["start"])
def start(message):
    z = ", ".join(komars)
    bot.send_message(message.chat.id, f"Доступные команды: \n{z}, карты, баланс")


@bot.message_handler(commands=["anoncment"])
def anoncment(message):
    if message.from_user.id != ME_ID:
        if message.from_user.id == 1472118418 or message.from_user.id == 7767572246:
            bot.send_message(message.from_user.id, "Мурчиков iдi нахуй")
            return
        else:
            bot.send_message(message.from_user.id, "Ты кто?")
            return

    users = methods.get_users_id()
    text = message.text.replace("/anoncment", "").strip()
    if not text:
        bot.send_message(message.from_user.id, "Введите текст для рассылки")
    for user in users:
        try:
            bot.send_message(user, text)
        except Exception as e:
            logging.error(f"Error anoncment {e}")
            bot.send_message(
                message.from_user.id, f"Ошибка при отправке сообщения {e} \nЮзер {user}"
            )

@bot.message_handler(commands=["komar"])
def komar(message):
    methods.generate_komar(message, bot)

@bot.message_handler(commands=["cards"])
def cards(message):
    markup = methods.generate_markup_cards(message)
    bot.send_message(message.chat.id, f"Выберите карточку:", reply_markup=markup)

@bot.message_handler(commands=["balance"])
def balance(message):
    bot.send_message(
            message.chat.id,
            f"Ваши монеты: {methods.get_user_money(message.from_user.id)[0]}",
        )

@bot.message_handler(content_types=["text"])
def text(message):
    if message.text.lower() in komars:
        methods.generate_komar(message, bot)

    if message.text.lower() == "карты":
        markup = methods.generate_markup_cards(message)
        bot.send_message(message.chat.id, f"Выберите карточку:", reply_markup=markup)

    if message.text.lower() == "баланс":
        bot.send_message(
            message.chat.id,
            f"Ваши монеты: {methods.get_user_money(message.from_user.id)[0]}",
        )


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data.startswith("card_"):
        data = callback.data.split("_")
        card_id = int(data[1])
        user_id = int(data[2])

        # Проверяем пользователя
        if callback.from_user.id != user_id:
            bot.answer_callback_query(callback.id, text="Это не ваша кнопка")
            return

        card = methods.get_card_by_id(card_id)
        markup = telebot.types.InlineKeyboardMarkup()

        name = card.get("name")
        rare = card.get("rare")
        money = card.get("money")
        img = card.get("img")

        markup.add(
            telebot.types.InlineKeyboardButton(
                text="Назад",
                callback_data=f"back",  # callback_data нужен для обработки нажатия
            )
        )

        bot.edit_message_media(
            chat_id=callback.message.chat.id,
            media=telebot.types.InputMediaPhoto(
                media=open(img, "rb"),
                caption=f"Карточка: {name}\nРедкость: {rare}\nСтоимость: {money} монет",
            ),
            message_id=callback.message.message_id,
            reply_markup=markup,
        )
    if callback.data == "back":
        markup = methods.generate_markup_cards(callback)
        bot.delete_message(
            chat_id=callback.message.chat.id, message_id=callback.message.message_id
        )
        bot.send_message(
            chat_id=callback.message.chat.id,
            text="Выберите карточку:",
            reply_markup=markup,
        )


logging.info(f"loggined as {bot.get_my_name().name}")

bot.polling()

logging.info("Bot stopped")
