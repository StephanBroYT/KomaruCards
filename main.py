import telebot, datetime, random, methods, logging

komars = ["комар", "комару", "komap", "komaru"]
# methods.setup_database()
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
    bot.send_message(message.chat.id, f"Доступные команды: \n{komars}, карты, монеты")


@bot.message_handler(commands=["anoncment"])
def anoncment(message):
    if message.from_user.id != 1127025574:
        if message.from_user.id == 1472118418 or message.from_user.id == 7767572246:
            bot.send_message(message.from_user.id, "Мурчиков iдi нахуй")
            return
        else:
            bot.send_message(message.from_user.id, "Ты кто?")
            return

    users = methods.get_users_id()
    print(users)
    text = message.text.replace("/anoncment", "").strip()
    if not text:
        bot.send_message(message.from_user.id, "Введите текст для рассылки")
    for user in users:
        try:
            bot.send_message(user, text)
        except Exception as e:
            print(f"Error anoncment {e}")
            bot.send_message(
                message.from_user.id, f"Ошибка при отправке сообщения {e} \nЮзер {user}"
            )


@bot.message_handler(content_types=["text"])
def text(message):
    if message.text.lower() in komars:
        try:
            komar_id = random.choice(list(methods.get_cards()))
            komar_data = methods.get_card_by_id(komar_id)

            name = komar_data.get("name")
            rare = komar_data.get("rare")
            money = komar_data.get("money")
            img = komar_data.get("img")

            logging.info(f"id:{komar_id} data:{komar_data}")
            methods.add_card_to_user(message.from_user.id, komar_id)
            bot.send_photo(
                message.chat.id,
                open(img, "rb"),
                caption=f"Вам выпала карточка {name} \nРедкость: {rare} \nВам добавлено {money} монет \n||ID: {komar_id}||",
                parse_mode="MarkdownV2",
            )
        except Exception as e:
            logging.error(f"Error {e}")

    if message.text.lower() == "карты":
        markup = methods.generate_markup_cards(message)
        bot.send_message(message.chat.id, f"Выберите карточку:", reply_markup=markup)

    if message.text.lower() == "монеты":
        bot.send_message(
            message.chat.id,
            f"Ваши монеты: {methods.get_user_money(message.from_user.id)}",
        )


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data.startswith("card_"):
        card_id = int(callback.data.split("_")[1])

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
                caption=f"Карточка: {name}\nРедкость: {rare}\nСтоимость: {money}",
            ),
            message_id=callback.message.message_id,
            reply_markup=markup,
        )
    if callback.data == "back":
        markup = methods.generate_markup_cards(callback)
        bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
        bot.send_message(
            chat_id=callback.message.chat.id,
            text="Выберите карточку:",
            reply_markup=markup,
        )


logging.info(f"""loggined as {bot.get_my_name().name}""")

bot.polling()

logging.info("Bot stopped")
