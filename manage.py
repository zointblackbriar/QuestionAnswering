from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from webapp import RestService, db
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)
from webapp.ModelWebApp import User

migrate = Migrate(RestService, db)
manager = Manager(RestService)

#migrations
manager.add_command('db', MigrateCommand)

@manager.command
def create_db():
    logger.info("Db is created")
    db.create_all()

@manager.command
def drop_db():
    logger.info("Db is dropped")
    db.drop_all()

@manager.command
def create_admin():
    logger.info("Db create admin operation")
    db.session.add(User(email='admin@admin.com', password='admin', admin=True))
    db.session.commit()

@manager.command
def create_data():
    logger.info("create data is not implemented")
    pass

if __name__ == '__main__':
    logger.info("server started from the command line")
    manager.run()
