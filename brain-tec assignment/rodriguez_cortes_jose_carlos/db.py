import mysql.connector as sqlc
import click
from flask import current_app, g
from flask.cli import with_appcontext

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

def get_db():
    if 'db' not in g:
        g.db = sqlc.connect(
            user = current_app.config['USER'],
            password = current_app.config['PASSWORD'],
            host = current_app.config['HOST'],
            port = current_app.config['PORT'],
        )
        return g.db

def close_db(paramenter = None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    cr = db.cursor()
    with current_app.open_resource(current_app.config['SQL_FILE']) as sql_file:
        for a in sql_file.read().decode('utf8').split("\n"):
            cr.execute(a)
        #cr.execute(sql_file.read().decode('utf8'), multi=True) # I considered this but doesn't work.
    db.commit()
    

@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo("Database Initialized")
