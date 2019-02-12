#import os
import logging
from logging.config import dictConfig

import yaml
import aiotask_context as context

from lemo import config


class RequestIdFilter(logging.Filter):
	def filter(self, record):
		try:
			record.request_id = context.get('X-Request-ID', default='n/a')
		except ValueError:
			record.request_id = 'n/a'
		return True


old_factory = logging.getLogRecordFactory()
def record_factory(*args, **kwargs):
	record = old_factory(*args, **kwargs)
	try:
		record.request_id = context.get('X-Request-ID', default='n/a')
	except ValueError:
		record.request_id = 'n/a'
	return record


def initialize():
	cfg = config.load()
	#print(os.listdir())
	with open('lemo/log_config.yml') as f:
		log_config = yaml.load(f.read())

	#log_config['filters']['request_id']['()'] = RequestIdFilter
	log_config['loggers']['']['level'] = cfg['log_level']

	dictConfig(log_config)
	logging.setLogRecordFactory(record_factory)


def get_logger(name):
	return logging.getLogger(name)
