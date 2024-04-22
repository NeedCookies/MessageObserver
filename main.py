import imaplib
import email
import telebot # установите в свое окружение библиотеку pip install PyTelegramBotAPI
import requests
import schedule
from MyData import myToken, myEmail, MyAppPass

#myToken = os.getenv('TOKEN')
#myEmail = os.getenv('EMAIL')
#MyAppPass = os.getenv('PASS')
if (myToken is None or myEmail is None or MyAppPass is None or
    len(myToken) == 0 or len(myEmail) == 0 or len(MyAppPass) == 0):
    raise Exception("One or more env var is empty")

def get_all_chats(botToken: str) -> []:
    url = f"https://api.telegram.org/bot{botToken}/getUpdates"
    response = requests.get(url)
    data = response.json()
    chat_ids = []
    for ch in data['result']:
        chat_id = ch['message']['chat']['id']
        chat_ids.append(chat_id)
    return chat_ids

def sendAllUsers(bot, mess, chats):
    for chat in chats:
        bot.send_message(chat, mess)

def getNewMess():
    bot = telebot.TeleBot(myToken)
    chat_ids = get_all_chats(myToken)

    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(myEmail, MyAppPass)
    mail.list()
    mail.select('Inbox')
    result, data = mail.uid('search', None, 'UNSEEN')

    messages = data[0].split()
    i = len(messages)
    for x in range(i):
        latest_email_uid = messages[x]
        result, email_data = mail.uid('fetch', latest_email_uid, '(RFC822)')
        raw_email = email_data[0][1]
        #mail.store(latest_email_uid, '+FLAGS', '\Deleted') # удаляем чтоб не было повторной отправки
        raw_email_string = raw_email.decode('unicode-escape')
        email_message = email.message_from_string(raw_email_string)
        for part in email_message.walk():
            if part.get_content_type() == "text/html" or part.get_content_type() == "text/plain":
                body = part.get_payload(decode=True)
                decBody = body.decode('utf-8')
                s = (email_message['Subject'])
                numb = s[5:16]
                mess = str(body.decode('utf-8'))
                abon = mess[54:67]
                smss = mess[77:]
                sendAllUsers(bot, mess, chat_ids)
            else:
                continue

def main():
    schedule.every(20).seconds.do(getNewMess)
    #schedule.every().day.at('03:00').do(getNewMess)
    while True:
        schedule.run_pending()

    #getNewMess()

if __name__ == '__main__':
    main()
