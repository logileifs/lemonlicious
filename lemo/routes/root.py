from sanic import response
from sanic.views import HTTPMethodView


class Root(HTTPMethodView):

	async def get(self, request):
		return response.json({'hello': 'world'})


route = (Root.as_view(), '/')
