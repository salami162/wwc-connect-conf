import gevent.monkey
gevent.monkey.patch_all()

from flask.ext.script import Manager

from connect import app
# from connect.utils.kmeans import write_data_csv

manager = Manager(app)
# manager.add_command('kmean', write_data_csv)

if __name__ == '__main__':
    manager.run()
