import threading
from flask import render_template, copy_current_request_context, current_app
from flask_mail import Message
from bookcrossing.mail import mail


def create_message(to, subject, username):
    msg = Message(subject,
                  sender='BookCros Admin <plaaark@yandex.ua>',
                  recipients=[to])
    msg.html = 'Dear {}! Welcome to BookCros service'.format(username)
    return msg


def send_email(to, subject, username):
    message = create_message(to, subject, username)
    mail.send(message)


def send_async_email(to, subject, username):
    message = create_message(to, subject, username)

    @copy_current_request_context
    def send_message(message):
        mail.send(message)

    thr = threading.Thread(name='email', target=send_message, args=(message,))
    thr.start()