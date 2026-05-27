from app.shared.database.extensions import db


class Position(db.Model):
    __tablename__ = "positions"
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)