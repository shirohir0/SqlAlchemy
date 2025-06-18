from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import List, Optional, Self  # Python 3.11+ (для Self типа)
from database_engine import Base
from sqlalchemy.orm import validates

from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from sqlalchemy import ForeignKey
from typing import List, Optional, Self
from database_engine import Base

class UsersOrm(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    age: Mapped[Optional[int]]
    gender_id: Mapped[int] = mapped_column(ForeignKey("genders.id", ondelete="SET NULL"), nullable=False)

    gender: Mapped["GendersORM"] = relationship(back_populates="users")

    # родительская запись (1:1)
    parents: Mapped[Optional["ParentsOrm"]] = relationship(
        "ParentsOrm",
        back_populates="user",
        uselist=False,
        foreign_keys="[ParentsOrm.user_id]"  # вот это обязательно!
    )


class ParentsOrm(Base):
    __tablename__ = "parents"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    mother_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"))
    father_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"))

    # основной пользователь, к которому относятся эти родители
    user: Mapped["UsersOrm"] = relationship(
        "UsersOrm",
        back_populates="parents",
        foreign_keys=[user_id]
    )

    mother: Mapped[Optional["UsersOrm"]] = relationship("UsersOrm", foreign_keys=[mother_id])
    father: Mapped[Optional["UsersOrm"]] = relationship("UsersOrm", foreign_keys=[father_id])


    # # === Мать ===
    # mother_id: Mapped[Optional[int]] = mapped_column(
    #     ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    # )
    # mother: Mapped[Optional[Self]] = relationship(
    #     "UsersOrm",
    #     remote_side=[id],
    #     back_populates="children_as_mother",
    #     foreign_keys="[UsersOrm.mother_id]"
    # )
    # children_as_mother: Mapped[List[Self]] = relationship(
    #     "UsersOrm",
    #     back_populates="mother",
    #     foreign_keys="[UsersOrm.mother_id]"
    # )

    # # === Отец ===
    # father_id: Mapped[Optional[int]] = mapped_column(
    #     ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    # )
    # father: Mapped[Optional[Self]] = relationship(
    #     "UsersOrm",
    #     remote_side=[id],
    #     back_populates="children_as_father",
    #     foreign_keys="[UsersOrm.father_id]"
    # )
    # children_as_father: Mapped[List[Self]] = relationship(
    #     "UsersOrm",
    #     back_populates="father",
    #     foreign_keys="[UsersOrm.father_id]"
    # )

    # # === Пол (Gender) ===
    # gender_id: Mapped[int] = mapped_column(ForeignKey("genders.id", ondelete="CASCADE"))
    # gender: Mapped["GendersORM"] = relationship("GendersORM", back_populates="users")

    # === Валидация ===
    @validates("mother_id", "father_id")
    def validate_parents(self, key, value):
        if value is not None and value == self.user_id:
            raise ValueError(f"{key} не может быть равен самому себе")
        return value



class GendersORM(Base):
    __tablename__ = 'genders'

    id: Mapped[int] = mapped_column(primary_key=True)
    gender: Mapped[str] = mapped_column(nullable=False)
    users: Mapped[list["UsersOrm"]] = relationship(
        back_populates="gender"
    )
    # users: Mapped[List['UsersOrm']] = relationship("UsersOrm", back_populates='gender')

