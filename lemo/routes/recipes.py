import uuid
import logging

from sanic import response
#from sanic import Blueprint
from sanic.views import HTTPMethodView as Route

#bp = Blueprint('my_blueprint')
#bp = Blueprint('content_authors', url_prefix='/users')

log = logging.getLogger(__name__)


class Recipes(Route):

	recipes = []

	async def get(self, request):
		"""
		get all users
		"""
		log.info('recipes get request: %s' % request)
		return response.json({'recipes': self.recipes})

	async def post(self, request):
		"""
		create a new user
		"""
		new_recipe = {
			'id': str(uuid.uuid4()),
			'title': None,
			'tags': [],
			'author': None,
			'content': None,
			'ingredients': []
		}
		self.recipes.append(new_recipe)
		return response.json({'recipe': new_recipe})


route = (Recipes.as_view(), '/recipes')
