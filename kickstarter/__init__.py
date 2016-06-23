from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Manager

app = Flask(__name__)
app.config.from_object('kickstarter.default_settings')
manager = Manager(app)

db = SQLAlchemy(app)
migrate = Migrate(app,db)
manager.add_command('db',MigrateCommand)

@app.route('/')
def hello_world():
    return render_template("index.html")