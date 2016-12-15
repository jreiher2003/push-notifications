from flask_script import Manager, Server
from pastebin import app, db


manager = Manager(app)
server = Server(host="0.0.0.0", port=5020)

manager.add_command("runserver", server)

@manager.command
def initdb():
    """Creates all database tables."""
    db.create_all()


@manager.command
def dropdb():
    """Drops all database tables."""
    db.drop_all()


if __name__ == '__main__':
    manager.run()
