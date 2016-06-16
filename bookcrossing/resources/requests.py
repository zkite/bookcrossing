from flask_restful import Resource
from bookcrossing import current_user
from bookcrossing import db
from bookcrossing.models.requests import RequestModel, RequestSchema
from bookcrossing.models.book import BookModel, BookSchema
from bookcrossing.models.user import UserModel
from bookcrossing.forms.select import SelectForm
from flask import render_template, request, make_response

from bookcrossing.utils.request_utils import (create_book_request,
                                              remove_request,
                                              update_request,
                                              get_requests_by_category)


class RequestsResource(Resource):
	def __init__(self):
		self.headers = {'Content-Type': 'text/html'}

	def get(self):
		select_category = request.values.get('select')
		requests = None
		if select_category:
			requests = get_requests_by_category(select_category, RequestModel, RequestSchema, BookModel, current_user, UserModel)

		return make_response(render_template('requests.html', requests=requests, category=select_category),
		                     200,
		                     self.headers)

	def post(self, book_id):

		if not current_user.id or not book_id:
			return make_response('requester_id or book_id ADD ERROR')

		request_object = create_book_request(book_id,
	                                         current_user,
		                                     BookModel,
		                                     RequestModel,
	                                         db)
		if request_object:
			'''
			send_notification_email_created_book_request(book_id,
													 requester_id)
			'''
			# print(request_object)
			# return make_response('Book Request OK, MSG SEND')
			return {'request_id':request_object.id}
		else:
			print(request_object)
			return make_response('Book Req ADD ERROR')

	def put(self, req_id):
		parsed_book = None
		print(req_id)
		book_req_obj = update_request(req_id, db, RequestModel, BookModel)
		print(book_req_obj)
		if book_req_obj:
			parsed_book = BookSchema().dump(book_req_obj).data
			parsed_book['title'] = BookModel.query.get(book_req_obj.book_id).title
			parsed_book['accept_date'] = book_req_obj.accept_date.strftime("%y-%m-%d-%H-%M")
			parsed_book['request_date'] = book_req_obj.request_date.strftime("%y-%m-%d-%H-%M")
			parsed_book['requester'] = UserModel.query.get(book_req_obj.req_user_id).login
			parsed_book['accepter'] = UserModel.query.get(book_req_obj.owner_user_id).login
			import json
			return json.dumps(parsed_book)
		else:
			return make_response('OOps BookRequest Update Error')

	def delete(self, request_id=None):
		if not request_id:
			return make_response('Request_id DELETE ERROR')
		rem_req = remove_request(request_id)
		if rem_req:
			return make_response('Book Req DELETE OK')
		else:
			return make_response('Book Req DELETE ERROR')


class RequestProfileResource(Resource):
	def get(self, book_id, req_id):
		print(book_id, req_id)
		return {'bok_id': book_id, 'req_id': req_id}