from gevent import monkey
monkey.patch_all()

import django
django.setup()

import logging

from django.conf import settings
from gevent.wsgi import WSGIServer
from raven.contrib.flask import Sentry

from gchatautorespond.lib.chatworker import Worker, app


if __name__ == '__main__':
    worker = Worker()
    worker.load()

    app.config['worker'] = worker

    sentry = Sentry(app, dsn=settings.RAVEN_CONFIG['dsn'],
                    logging=True, level=logging.ERROR)

    server = WSGIServer(('127.0.0.1', settings.WORKER_PORT), app)
    server.serve_forever()