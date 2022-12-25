from .base import TimestampModel, UUIDModel
from sqlmodel import Field



class User(UUIDModel, TimestampModel, table=True):
    __tablename__ = "user"

    first_name: str
    last_name: str
    email: str = Field(sa_column_kwargs={"unique": True})
    password: str
    email_verified : bool = False
    # is_admin : bool = False 

    def __repr__(self):
        return f"<User (id: {self.id})>"


