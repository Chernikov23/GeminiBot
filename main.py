import telebot
import google.generativeai as genai
import data


telegramToken = data.gemToken

bot = telebot.TeleBot(telegramToken)
genai.configure(api_key="AIzaSyBrMJYCoOguB2rDEn1B9JsYnbf-Ot_Pp-U")
model = genai.GenerativeModel('gemini-pro')


@bot.message_handler(commands=["start"])
def start(message):
    ans = f"{message.from_user.username}, Привет! Я, пока что, тестовая модель телеграмм бота с Gemini. Если я плохо отвечаю, то не судите строго. я еще учусь"
    bot.send_message(message.chat.id, ans)


@bot.message_handler(commands=["get_chat_id"])
def get_chat_id(message):
    try:
        chat_id = message.chat.id
        bot.send_message(message.chat.id, f"Your chat ID is: {chat_id}")
    except Exception as e:
        bot.send_message(message.chat.id, f"Error getting chat ID: {str(e)}")


sent_chat_ids = set()


@bot.message_handler(commands=["send_to_all"])
def send_to_all(message):
    try:
        users_file = "ides.txt"
        with open(users_file, "r") as f:
            users = f.readlines()
            for user in users:
                user = user.strip()
                try:
                    chat_id = bot.get_chat(user).id
                    if chat_id not in sent_chat_ids:
                        print(f"Sending message to {user} with chat_id {chat_id}")
                        bot.send_message(chat_id, "Данный Бот меняется и теперь у него новый адрес в телеграмм: @GeminiAIGoogleSyBot или https://t.me/GeminiAIGoogleSyBot" )
                            # Добавляем ID чата в список уже отправленных
                        sent_chat_ids.add(chat_id)
                    else:
                        print(f"Message already sent to {user} with chat_id {chat_id}")
                except Exception as e:
                    print(f"Error sending message to {user}: {str(e)}")
    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка при отправке сообщения пользователям: {str(e)}")


@bot.message_handler(func=lambda message: True)
def handleText(message):
    try:
        with open("notifications.txt", "a") as f:
            f.write(f"{message.from_user.username}: {message.text}\n")
            f.write("\n")
            f.close()
        with open("ides.txt", "a") as f:
            f.write(f"{message.chat.id}\n")
            f.write("\n")
            f.close()
        print(f"{message.from_user.username} ({message.chat.id}): {message.text}")
        que = message.text

        response = model.generate_content(que)

        bot.send_message(message.chat.id, response.text)
        with open("notifications.txt", "a") as f:
            f.write(f"Ответ Gemini: {response.text} \n")
            f.write("\n")
            f.close()
    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка про обработке вашего запроса: {str(e)}")
        with open("notifications.txt", "a") as f:
            f.write(f"Ответ Gemini: Произошла ошибка про обработке вашего запроса: {str(e)} \n")
            f.write("\n")
            f.close()


bot.polling(none_stop=True)
