from flask.views import View
from flask import render_template

class ListView(View):
    """A generic ListView.
    TODO: figure out how to pass ordering
    """
    def __init__(self, model):
        self.model = model
        self.template = f"{model.__name__.lower()}/list.html"

    def dispatch_request(self):
        items = self.model.query
        return render_template(self.template, items=items)


class DetailView(View):
    def __init__(self, model):
        self.model = model
        self.template = f"{model.__name__.lower()}/detail.html"

    def dispatch_request(self, id):
        item = self.model.query.get_or_404(id)
        return render_template(self.template, item=item)
