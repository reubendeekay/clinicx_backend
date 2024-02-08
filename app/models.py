from .database import Base
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    DateTime,
    Boolean,
    Float,
    Enum,
)
from sqlalchemy.types import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship
from .enums import Gender, Role, MaritalStatus, BloodGroup


class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    is_active = Column(Boolean, server_default="TRUE", nullable=False)
    appointments = relationship("Appointment", back_populates="service")
    doctors = relationship("Doctor", back_populates="service")
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=text("NOW()"), nullable=False
    )


class Branch(Base):
    __tablename__ = "branches"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    address = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    longitude = Column(Float, nullable=False)
    latitude = Column(String, nullable=False)
    is_active = Column(Boolean, server_default="TRUE", nullable=False)
    doctors = relationship("Doctor", back_populates="branch")
    appointments = relationship("Appointment", back_populates="branch")
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=text("NOW()"), nullable=False
    )


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    is_active = Column(Boolean, server_default="TRUE", nullable=False)
    gender = Column(Enum(Gender), default=Gender.MALE)
    marital_status = Column(Enum(MaritalStatus), default=MaritalStatus)
    user_image = Column(String, nullable=False)
    date_of_birth = Column(String, nullable=False)
    role = Column(Enum(Role), default=Role.PATIENT)
    doctors = relationship("Doctor", back_populates="user")
    is_active = Column(Boolean, server_default="TRUE", nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=text("NOW()"), nullable=False
    )


class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, nullable=False)
    branch_id = Column(Integer, ForeignKey("branches.id"))
    branch = relationship("Branch", back_populates="doctors")
    is_active = Column(Boolean, server_default="TRUE", nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    service_id = Column(Integer, ForeignKey("services.id"))

    user = relationship("User", back_populates="doctors")
    service = relationship("Service", back_populates="doctors")
    appointments = relationship("Appointment", back_populates="doctor")
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=text("NOW()"), nullable=False
    )


class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    phone_number = Column(String, nullable=False, unique=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    is_active = Column(Boolean, server_default="TRUE", nullable=False)
    gender = Column(Enum(Gender), default=Gender.MALE)
    marital_status = Column(Enum(MaritalStatus), default=MaritalStatus.SINGLE)
    user_image = Column(String, nullable=False)
    date_of_birth = Column(String, nullable=False)
    role = Column(Enum(Role), default=Role.PATIENT)
    is_active = Column(Boolean, server_default="TRUE", nullable=False)
    address = Column(String, nullable=False)
    blood_group = Column(Enum(BloodGroup), default=BloodGroup.A_POSITIVE)
    about = Column(String, nullable=False)
    appointments = relationship("Appointment", back_populates="patient")
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=text("NOW()"), nullable=False
    )


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, nullable=False)
    is_active = Column(Boolean, server_default="TRUE", nullable=False)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    patient = relationship("Patient", back_populates="appointments")
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    doctor = relationship("Doctor", back_populates="appointments")
    service_id = Column(Integer, ForeignKey("services.id"))
    service = relationship("Service", back_populates="appointments")
    appointment_date = Column(String, nullable=False)
    appointment_time = Column(String, nullable=False)
    is_confirmed = Column(Boolean, server_default="FALSE", nullable=False)
    branch_id = Column(Integer, ForeignKey("branches.id"))
    branch = relationship("Branch", back_populates="appointments")
    reason = Column(String, nullable=False)
    payments = relationship("Payment", back_populates="appointment")
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=text("NOW()"), nullable=False
    )


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, nullable=False)
    is_active = Column(Boolean, server_default="TRUE", nullable=False)
    appointment_id = Column(Integer, ForeignKey("appointments.id"))
    appointment = relationship("Appointment", back_populates="payments")
    amount = Column(Integer, nullable=False)
    payment_mode = Column(String, nullable=False)
    discount = Column(Integer)
    is_paid = Column(Boolean, server_default="FALSE", nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=text("NOW()"), nullable=False
    )


class OTP(Base):
    __tablename__ = "otps"

    id = Column(Integer, primary_key=True, nullable=False)
    is_active = Column(Boolean, server_default="TRUE", nullable=False)
    user_id = Column(Integer, nullable=False)
    otp = Column(String, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=text("NOW()"), nullable=False
    )
