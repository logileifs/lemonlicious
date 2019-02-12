import glob
import logging
import importlib
from os import path

log = logging.getLogger(__name__)


def add_routes(app, routes_dir):
    package = path.abspath(__package__)
    log.debug('package: %s' % package)
    path_to_routes = path.join(package, routes_dir)
    log.debug('path_to_routes: %s' % path_to_routes)
    candidates = glob.glob(path_to_routes + '/*.py')
    log.debug('candidates: %s' % candidates)
    modules = [
        c.split('/')[-1]
        for c in candidates
        if not c.endswith('__init__.py')
    ]
    log.debug('modules: %s' % modules)
    for m in modules:
        mod_name = __package__ + '.' + routes_dir + '.' + m.split('.py')[0]
        mod = importlib.import_module(mod_name)
        log.debug('adding route: %s at %s' % (mod_name, mod.route[-1]))
        app.add_route(*mod.route)
