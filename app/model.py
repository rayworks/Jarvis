from . import db


class Todo(db.Model):
    __tablename__ = 'todo'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)

    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return '<todo %r>' % self.title
