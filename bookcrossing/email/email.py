import threading
from flask import copy_current_request_context
from bookcrossing import mail, Message


def create_message(to, subject, username):
	msg = Message(subject,
	              sender='BookCros Admin <book.crossing.adm@yandex.ru>',
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