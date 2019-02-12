import uuid
import asyncio

from lemo import config
from lemo import router
from lemo import logging

import uvloop
import sanic.exceptions
from sanic import Sanic
from sanic import response
import aiotask_context as context
from marshmallow.exceptions import ValidationError

cfg = config.load()
logging.initialize()
log = logging.get_logger(__name__)
app = Sanic()


@app.middleware('request')
async def set_request_id(request):
	request_id = request.headers.get('X-Request-ID') or str(uuid.uuid4())
	context.set("X-Request-ID", request_id)
	request.headers['X-Request-ID'] = request_id


@app.middleware('response')
async def set_response_id(request, response):
	response.headers['X-Request-ID'] = context.get('X-Request-ID')


@app.exception(ValidationError)
#@app.exception(sanic.exceptions.InvalidUsage)
async def handle_validation_error(request, err):
	log.info('handle_validation_error')
	return response.json({"errors": err.messages, 'status': 400}, status=400)


@app.exception(sanic.exceptions.ServerError)
async def handle_server_error(request, err):
	log.info('handle_server_error')
	log.critical('exception: %s' % err)


if __name__ == '__main__':
	host = cfg['host']
	port = cfg['port']
	router.add_routes(app, 'routes')
	asyncio.set_event_loop(uvloop.new_event_loop())
	server = app.create_server(host=host, port=port)
	loop = asyncio.get_event_loop()
	loop.set_task_factory(context.task_factory)
	task = asyncio.ensure_future(server)
	log.info('running in dev mode on %s:%s' % (host, port))
	try:
		loop.run_forever()
	except Exception:
		loop.stop()

	#app.run(host=host, port=port)
