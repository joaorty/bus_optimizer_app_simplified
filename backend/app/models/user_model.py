from sqlalchemy import Column, Integer, String, TIMESTAMP, func
from sqlalchemy.orm import relationship
from app.utils import Base

class SolverUser(Base):
    __tablename__ = "solver_user"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())

    scenarios = relationship("Scenario", back_populates="solver_user", cascade="all, delete-orphan")

    def __init__(self, name, email, password_hash):
        self.name = name
        self.email = email
        self.password_hash = password_hash

    def __repr__(self):
        return f"<SolverUser(id={self.id}, email={self.email})>"

    def to_dict(self):
        try:
            scenarios = [s.to_dict() for s in self.scenarios]
        except:
            scenarios = []  # sessão fechada, evita crash

        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "password_hash": self.password_hash,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "scenarios": scenarios
        }