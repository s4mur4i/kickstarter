from flask import Flask, render_template, request, redirect, url_for, abort
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Manager
from flask.ext.sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
app.config.from_object('kickstarter.default_settings')
manager = Manager(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

from kickstarter.models import *


@app.route('/')
def hello():
    return render_template("index.html")


@app.route('/projects/create/', methods=['GET', 'POST'])
def create():
    if request.method == "GET":
        return render_template("create.html")
    elif request.method == "POST":
        # Form submission
        now = datetime.datetime.now()
        time_end = request.form.get("funding_end_date")
        print(time_end)
        time_end = datetime.datetime.strptime(time_end, "%Y-%m-%d")
        new_project = Project(member_id=1, name=request.form.get("project_name"),
                              short_description=request.form.get("short_description"),
                              long_description=request.form.get("long_description"),
                              goal_amount=request.form.get("funding_goal"), time_start=now, time_end=time_end,
                              time_created=now)
        db.session.add(new_project)
        db.session.commit()

        return redirect(url_for('project_detail', project_id=new_project.id))


@app.route("/projects/<int:project_id>/")
def project_detail(project_id):
    project = db.session.query(Project).get(project_id)
    if project is None:
        abort(404)
    return render_template("project_detail.html", project=project)
