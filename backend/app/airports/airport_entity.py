from app.shared.database.extensions import db


class Airport(db.Model):
    __tablename__ = "airports"
    id = db.Column(db.String(36), primary_key=True)