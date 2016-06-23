from kickstarter import db


class Member(db.model):
    id = db.Column(db.Integer,primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    project = db.relationship('Project', backref='creator')
    pledges = db.relationship('Pledge', backref='pledger',foreign_key='Pledge.member_id')

class Project(db.model):
    id = db.Column(db.Integer,primary_key=True)
    member_id = db.Column(db.Integer,db.ForeignKey('member.id'),nullable=False)
    name = db.Column(db.String(100))
    short_descriptin = db.Column(db.Text)
    long_descriptin = db.Column(db.Text)
    goal_amount = db.Column(db.Integer)
    time_start = db.Column(db.DateTime)
    time_end = db.Column(db.DateTime)
    time_created = db.Column(db.DateTime)
    pledges = db.relationship('Pledge', backref='project',foreign_key='Pledge.project_id')


class Pledge(db.model):
    id = db.Column(db.Integer,primary_key=True)
    member_id = db.Column(db.Integer,db.ForeignKey('member.id'),nullable=False)
    project_id = db.Column(db.Integer,db.ForeignKey('project.id'),nullable=False)
    amount = db.Column(db.Integer)
    time_created = db.Column(db.DateTime)