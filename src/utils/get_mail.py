import imaplib
import email
from email.header import decode_header


def get_last_emails(username, password, imap_server='imap.mail.ru', num_messages=5):
    # Создаем SSL-соединение
    mail = imaplib.IMAP4_SSL(imap_server)

    try:
        # Авторизация
        mail.login(username, password)

        # Выбираем папку "Входящие"
        mail.select('inbox')

        # Получаем общее количество писем
        status, messages = mail.search(None, 'ALL')
        messages = messages[0].split()

        # Получаем последние N писем (отсчитываем с конца)
        last_messages = messages[-num_messages:]

        # Получаем и обрабатываем каждое письмо
        for num in last_messages:
            status, msg = mail.fetch(num, '(RFC822)')
            for response in msg:
                if isinstance(response, tuple):
                    # Парсим письмо
                    raw_message = response[1]
                    email_message = email.message_from_bytes(raw_message)

                    # Декодируем тему письма
                    subject, encoding = decode_header(email_message['Subject'])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding)

                    # Получаем дату письма
                    date = email_message['Date']

                    # Получаем отправителя
                    sender = email_message['From']

                    print(f"Тема: {subject}")
                    print(f"Отправитель: {sender}")
                    print(f"Дата: {date}")
                    print("-" * 50)

    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")
    finally:
        # Закрываем соединение
        mail.close()
        mail.logout()


# Пример использования
get_last_emails(
    username="dolgov_am@mail.ru",
    password="f8VBe9HfySiteFUAhiAM"
)