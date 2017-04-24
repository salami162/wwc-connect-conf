import gevent.monkey
gevent.monkey.patch_all()

from flask.ext.script import Manager

from connect import app

manager = Manager(app)

if __name__ == '__main__':
    manager.run()
