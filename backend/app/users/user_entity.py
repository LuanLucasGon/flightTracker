from app.shared.database.extensions import db


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.String(36), primary_key=True)