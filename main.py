import telebot, datetime, random, methods, logging

komars = ["комар", "комару", "komap", "komaru"]
# methods.setup_database()
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(message)s',
    datefmt="%d/%m/%Y %I:%M:%S %p",
    handlers=[
        logging.FileHandler("./logs.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

bot = telebot.TeleBot("7790065715:AAEJO6VcuvW03QwcWJDER1Ie5LNv1XY1uxg")


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, f"Доступные команды: \n{komars}, карты")


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

            logging.info(f'id:{komar_id} data:{komar_data}')
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
        cards = "\n"
        for i in methods.get_user_cards(message.from_user.id):
            card = methods.get_card_by_id(i)
            cards += f"{card.get('name')} {card.get('rare')}\n"
        bot.send_message(message.chat.id, f"Ваши карточки: {cards}")


logging.info(f"""loggined as {bot.get_my_name().name}""")

bot.polling()

logging.info("Bot stopped")
