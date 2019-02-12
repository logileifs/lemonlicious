import yaml


# TODO: insert borg class here


def load():
	with open('config.yml') as stream:
		config = yaml.load(stream)
	return config
