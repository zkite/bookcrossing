from flask_mail import Message
from bookcrossing.mail import mail


def send_email(to, subject, username):
    msg = Message(subject,
                  sender='BookCros Admin <plaaark@yandex.ua>',
                  recipients=[to])
    msg.html = 'Dear {}! Welcome to BookCros service'.format(username)
    mail.send(msg)
