from app.shared.database.extensions import db


class Ticket(db.Model):
    __tablename__ = "tickets"
    id = db.Column(db.String(36), primary_key=True)