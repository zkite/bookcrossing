from bookcrossing.views.base_view import BaseMethodView
from bookcrossing.models.request_history import RequestHistoryModel

class BaseRequestHistoryView(BaseMethodView):
    def get_request_history(self):
        return RequestHistoryModel.query.all()