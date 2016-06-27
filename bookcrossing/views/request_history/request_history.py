from flask import make_response, render_template

from bookcrossing.views.request_history.base_request_history import BaseRequestHistoryView

class RequestHistoryView(BaseRequestHistoryView):
    def get(self):
        requests = self.get_request_history()
        return make_response(render_template("request_history.html", request_details = requests), 200)