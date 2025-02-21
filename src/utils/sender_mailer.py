import smtplib
from email.message import EmailMessage


def send_email(subject, body, sender, recipient, password):
    # Создаем сообщение
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient

    # Устанавливаем соединение с правильным портом и таймаутом
    server = smtplib.SMTP_SSL('smtp.mail.ru', 465, timeout=30)

    try:
        # Авторизация
        server.login(sender, password)

        # Отправка письма
        server.send_message(msg)
        print("Письмо успешно отправлено!")

    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")
    finally:
        server.quit()


# Пример использования
send_email(
    "Тестовое письмо",
    "Это тестовое сообщение",
    "dolgov_am@mail.ru",
    "gakusei96@mail.ru",
    "f8VBe9HfySiteFUAhiAM"
)