import gevent.monkey
gevent.monkey.patch_all()


from flask.ext.script import Manager

from connect import app
from scripts.kmeans import KMeansCommand

manager = Manager(app)
manager.add_command('kmeans', KMeansCommand)

if __name__ == '__main__':
    manager.run()

