from sqlalchemy import Column, Integer, ForeignKey, Text, TIMESTAMP, func
from sqlalchemy.orm import relationship
from app.utils import Base

class Scenario(Base):
    __tablename__ = "scenario"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("solver_user.id", ondelete="CASCADE"), nullable=False)
    name = Column(Text, nullable=False)
    description = Column(Text)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())

    solver_user = relationship("SolverUser", back_populates="scenarios")
    routes = relationship("Route", back_populates="scenario", cascade="all, delete-orphan")
    solution = relationship("Solution", uselist=False, back_populates="scenario", cascade="all, delete-orphan")
    bus_types = relationship("BusType", back_populates="scenario", cascade="all, delete-orphan")
    parameters = relationship("Parameters", back_populates="scenario", cascade="all, delete-orphan")

    def __init__(self, user_id, name, description=None):
        self.user_id = user_id
        self.name = name
        self.description = description

    def __repr__(self):
        return f"<Scenario(id={self.id}, name={self.name})>"

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "routes": [route.to_dict() for route in self.routes],
            "solution": self.solution.to_dict() if self.solution else None,
            "bus_types": [bus_type.to_dict() for bus_type in self.bus_types],
            "parameters": [parameter.to_dict() for parameter in self.parameters],
        }
