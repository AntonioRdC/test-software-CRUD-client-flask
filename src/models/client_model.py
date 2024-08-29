from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String

from database.database import db


class Client(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    cpf: Mapped[str] = mapped_column(String, unique=True)
    street: Mapped[str] = mapped_column(String)
    number: Mapped[str] = mapped_column(String)
    complement: Mapped[str] = mapped_column(String)
    neighborhood: Mapped[str] = mapped_column(String)
    zip_code: Mapped[str] = mapped_column(String)
    city: Mapped[str] = mapped_column(String)
    state: Mapped[str] = mapped_column(String)
    phone: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String)

    __table_args__ = {'extend_existing': True}

    def __init__(self, name, cpf, street, number, complement, neighborhood, zip_code, city, state, phone, email):
        self.name = name
        self.cpf = cpf
        self.email = email
        self.phone = phone
        self.street = street
        self.number = number
        self.complement = complement
        self.neighborhood = neighborhood
        self.zip_code = zip_code
        self.city = city
        self.state = state
