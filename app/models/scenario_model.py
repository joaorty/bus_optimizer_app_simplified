from sqlalchemy import Column, Integer, Text, TIMESTAMP, func
from sqlalchemy.orm import relationship
from .base import Base

class Scenario(Base):
    __tablename__ = "scenario"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, nullable=False)
    description = Column(Text)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())

    routes = relationship("Route", back_populates="scenario", cascade="all, delete-orphan")
    solutions = relationship("Solution", back_populates="scenario", cascade="all, delete-orphan")
    bus_types = relationship("BusType", back_populates="scenario", cascade="all, delete-orphan")
    parameters = relationship("Parameters", back_populates="scenario", cascade="all, delete-orphan")

    def __init__(self, name, description=None):
        self.name = name
        self.description = description

    def __repr__(self):
        return f"<Scenario(id={self.id}, name={self.name})>"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
