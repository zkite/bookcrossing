from flask import render_template, make_response
from flask_restful import Resource

class Index(Resource):
	def __init__(self):
		self.headers = {'Content-Type': 'text/html'}

	def get(self):
		return make_response(render_template('index.html'), 200, self.headers)
