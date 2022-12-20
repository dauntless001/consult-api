from .base import TimestampModel, UUIDModel


class User(UUIDModel, TimestampModel, table=True):
    __tablename__ = "user"

    first_name: str
    last_name: str
    email: str
    password: str

    def __repr__(self):
        return f"<User (id: {self.id})>"


