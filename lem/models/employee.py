import datetime

from lem import db


def dump_datetime(value):
    """Deserialize datetime object into string form for JSON processing."""
    if value is None:
        return None
    return value.strftime("%Y-%m-%d %H:%M:%S")


class Employee(db.Model):
    __tablename__ = 'employee'

    DATA_GROUPS = 'groups'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, index=True, unique=True)
    department = db.Column(db.String(255), nullable=False)
    created_dt = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    updated_dt = db.Column(db.DateTime, onupdate=datetime.datetime.utcnow, nullable=True)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'department': self.department,
            'created_dt': dump_datetime(self.created_dt),
            'updated_dt': dump_datetime(self.updated_dt)
        }

    @property
    def serialize_many2many(self):
        """
        Return object's relations in easily serializeable format.
        NB! Calls many2many's serialize property.
        """
        return [item.serialize for item in self.many2many]
