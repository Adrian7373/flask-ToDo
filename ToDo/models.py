from flask_login import UserMixin
from ToDo import db, login_manager, bcrypt

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String(60), nullable=False)
    owned_folders = db.relationship('Folder', backref='owned_user', lazy=True)

    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute")

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, plain_text_password):
        return bcrypt.check_password_hash(self.password_hash, plain_text_password)


class Folder(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    color = db.Column(db.String(), default="#69D7E6")
    tasks = db.relationship('Task', backref='folder', cascade='all, delete-orphan', lazy='dynamic')
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))

class Task(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(300), nullable=True)
    is_completed = db.Column(db.Boolean, default=False)
    datetime_completed = db.Column(db.DateTime)
    dueDate = db.Column(db.DateTime, nullable=True)
    folder_id = db.Column(db.Integer, db.ForeignKey('folder.id'), nullable=False)
    subtasks = db.relationship('Subtask', backref="task", cascade="all, delete-orphan", lazy='dynamic')

class Subtask(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    is_completed = db.Column(db.Boolean, default=False)
    datetime_completed = db.Column(db.DateTime)
    task_id = db.Column(db.Integer(), db.ForeignKey('task.id'), nullable=False)

