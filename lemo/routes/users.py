import logging
#from http import HTTPStatus

from sanic import response
#from sanic.exceptions import abort
#from sanic import Blueprint
from sanic.views import HTTPMethodView as Route
from marshmallow.exceptions import ValidationError

from lemo.models.user import User

#bp = Blueprint('my_blueprint')
#bp = Blueprint('content_authors', url_prefix='/users')

log = logging.getLogger(__name__)


class Users(Route):

	#users = []

	async def get(self, request):
		"""
		get all users
		"""
		log.info('user get request: %s' % request)
		users = User.all()
		log.info('users: %s' % users)
		return response.json({'users': users})

	async def post(self, request):
		"""
		create a new user
		"""
		try:
			log.info('creating new user with data: %s' % request.json)
			user = User(**request.json)
			user.save()
			log.info('user created: %s' % user.data)
		except ValidationError as err:
			log.info('invalid data %s' % err)
			raise err
			#abort(HTTPStatus.BAD_REQUEST, message=err.messages)
		return response.json({'user': user.data})


route = (Users.as_view(), '/users')
