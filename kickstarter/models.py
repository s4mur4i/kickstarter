from kickstarter import db, app
from sqlalchemy.sql import func
from flask.ext.security import RoleMixin, UserMixin
import datetime
import cloudinary.utils

roles_members = db.Table('roles_members',
                         db.Column('member_id', db.Integer(), db.ForeignKey('member.id')),
                         db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class Member(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    project = db.relationship('Project', backref='creator', lazy='dynamic')
    pledges = db.relationship('Pledge', backref='member', lazy='dynamic', foreign_keys='Pledge.member_id')
    roles = db.relationship('Role', secondary=roles_members,
                            backref=db.backref('members', lazy='dynamic'))


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False)
    name = db.Column(db.String(64), nullable=False)
    short_description = db.Column(db.Text, nullable=False)
    long_description = db.Column(db.Text, nullable=False)
    goal_amount = db.Column(db.Integer, nullable=False)
    image_filename = db.Column(db.String(128), nullable=False)
    time_created = db.Column(db.DateTime(timezone=False), nullable=False)
    time_start = db.Column(db.DateTime(timezone=False), nullable=False)
    time_end = db.Column(db.DateTime(timezone=False), nullable=False)
    pledges = db.relationship('Pledge', backref='project', lazy='dynamic', foreign_keys='Pledge.project_id')
    rewards = db.relationship('Reward', backref='project', lazy='dynamic', foreign_keys='Reward.project_id')
    category_id = db.Column(db.INTEGER, db.ForeignKey('category.id'), nullable=True)

    @property
    def total_pledges(self):
        total_pledges = db.session.query(func.sum(Pledge.amount)).filter(Pledge.project_id == self.id).one()[0]
        if total_pledges is None:
            total_pledges = 0

        return total_pledges

    @property
    def num_pledges(self):
        return self.pledges.count()

    @property
    def num_days_left(self):
        now = datetime.datetime.now()
        num_days_left = (self.time_end - now).days

        return num_days_left

    @property
    def percentage_funded(self):
        return int(self.total_pledges * 100 / self.goal_amount)

    @property
    def image_path(self):
        return cloudinary.utils.cloudinary_url(self.image_filename)[0]

    @property
    def duration(self):
        return (self.time_end - self.time_start).days

    def get_num_pledges_datapoints(self):
        pledges_per_day = db.session.query(
            func.date(Pledge.time_created),
            func.count(Pledge.time_created)
        ).filter(
            Project.id == self.id,
            Project.id == Pledge.project_id
        ).group_by(
            func.date(Pledge.time_created)
        ).all()

        ret = [[i + 1, 0] for i in range(self.duration)]

        for p in pledges_per_day:
            time_pledged = datetime.datetime.strptime(p[0], '%Y-%m-%d')
            day_num = (time_pledged.date() - self.time_start.date()).days + 1
            num_pledges = p[1]
            ret[day_num] = [day_num, num_pledges]

        return ret

    def get_amount_pledged_datapoints(self):
        amount_per_day = db.session.query(
            func.date(Pledge.time_created),
            func.sum(Pledge.amount)
        ).filter(
            Project.id == self.id,
            Project.id == Pledge.project_id
        ).group_by(
            func.date(Pledge.time_created)
        ).all()

        ret = [[i + 1, 0] for i in range(self.duration)]

        for p in amount_per_day:
            time_pledged = datetime.datetime.strptime(p[0], '%Y-%m-%d')
            day_num = (time_pledged.date() - self.time_start.date()).days + 1
            amount = p[1]
            ret[day_num] = [day_num, amount]

        return ret


class Category(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    slug = db.Column(db.String(64), nullable=False)
    project = db.relationship('Project', backref='category', lazy='dynamic', foreign_keys='Project.category_id')

class Pledge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    reward_id = db.Column(db.Integer, db.ForeignKey('reward.id'), nullable=True)
    amount = db.Column(db.Integer, nullable=False)
    time_created = db.Column(db.DateTime(timezone=False), nullable=False)


class Reward(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    title = db.Column(db.String(64), nullable=False)
    description = db.Column(db.Text, nullable=False)
    minimum_pledge_amount = db.Column(db.Integer, nullable=False)
    pledges = db.relationship('Pledge', backref='reward', lazy='dynamic', foreign_keys='Pledge.reward_id')

    @property
    def num_pledges(self):
        return self.pledges.count()
