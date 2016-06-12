from flask_restful import Resource


# This is just example GET, POST methods working with render_template
class Index(Resource):

    def get(self):
        return ['Hello World']
