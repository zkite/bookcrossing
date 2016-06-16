import threading
from flask import copy_current_request_context, render_template
from bookcrossing import mail, Message


def create_message(to, subject, template, **kwargs):
    """
    def create_message(to, subject, template, **kwargs)
    :param to: recipient of the letter
    :param subject: content of the letter
    :param template: path to template
    :param kwargs: extra options (for example user name or etc.)
    :return: message to be send

    """
    msg = Message(subject,
                  sender='Bookcrossing Admin <admbookcross@yandex.ru>',
                  recipients=[to])
    msg.html = render_template(template + '.html', **kwargs)
    return msg


def send_email(to, subject, template, **kwargs):
    message = create_message(to, subject, template, **kwargs)
    mail.send(message)


def send_async_email(to, subject, template, **kwargs):
    message = create_message(to, subject, template, **kwargs)

    @copy_current_request_context
    def send_message(msg):
        mail.send(msg)

    thr = threading.Thread(name='email', target=send_message, args=(message,))
    thr.start()