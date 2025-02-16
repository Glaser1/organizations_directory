from sqlalchemy import String, CheckConstraint, ForeignKey, Table, Column, Index
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr, relationship


class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)

    @declared_attr.directive
    def __tablename__(cls):
        return f"{cls.__name__.lower()}s"


organization_activity = Table(
    "organization_activity",
    Base.metadata,
    Column("organization_id", ForeignKey("organizations.id"), primary_key=True),
    Column("activity_id", ForeignKey("activities.id"), primary_key=True),
)


class Organization(Base):
    title: Mapped[str] = mapped_column(unique=True)
    phones: Mapped[list["PhoneNumber"]] = relationship(
        back_populates="organization",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    building: Mapped["Building"] = relationship(back_populates="organizations")
    activities: Mapped[list["Activity"]] = relationship(
        secondary="organization_activity", back_populates="organizations"
    )
    building_id: Mapped[int] = mapped_column(ForeignKey("buildings.id"))


class PhoneNumber(Base):
    __tablename__ = "phone_numbers"

    phone: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"))
    organization: Mapped["Organization"] = relationship(back_populates="phones")


class Activity(Base):
    __tablename__ = "activities"

    title: Mapped[str]
    organizations: Mapped[list["Organization"]] = relationship(
        secondary="organization_activity", back_populates="activities"
    )
    children: Mapped[list["Activity"]] = relationship(back_populates="parent", lazy="selectin")
    parent_id: Mapped[int] = mapped_column(ForeignKey("activities.id"), nullable=True)
    parent: Mapped["Activity"] = relationship(back_populates="children", remote_side="Activity.id")

    __table_args__ = (CheckConstraint("parent_id != id", name="check_parent_id_not_equal_id"), Index("ix_activities_title", "title"),)


class Building(Base):
    address: Mapped[str] = mapped_column(String(200), unique=True)
    latitude: Mapped[float]
    longitude: Mapped[float]

    organizations: Mapped[list["Organization"]] = relationship(back_populates="building")
