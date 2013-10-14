import os
from flask.ext.script import Manager
from config import db
from app import create_app

app = create_app()
manager = Manager(app)
manager.add_command("runserver",Server("localhost",port=8000))

@manager.command
def init()
    dfile = 'database.db'
    if os.path.exists(dfile):
        os.remove(dfile)
    db.create_all()

if __name__ == "__main__":
    manager.run()
