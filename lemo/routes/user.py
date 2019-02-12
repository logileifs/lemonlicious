
from sanic import response
from sanic.views import HTTPMethodView as Route


class User(Route):
	async def get(self, request, uid):
		"""
		get a single user
		"""
		return response.json(
			{'id': uid, 'name': None, 'email': None}
		)


route = (User.as_view(), '/user/<uid>')
