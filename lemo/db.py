import rethinkdb as rt


def connect(host='localhost', port=28015, db='test'):
	conn = rt.connect(host, port).repl()
	try:
		rt.db_create(db).run(conn)
	except rt.errors.ReqlOpFailedError:
		print('db already exists')
	#r.db(db).table_create('tv_shows').run()
	return conn
