from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime
from .enums import Gender, Role, MaritalStatus, BloodGroup


class BranchBase(BaseModel):

    name: str
    description: str
    address: str
    phone_number: str
    longitude: float
    latitude: float

    class Config:
        orm_mode = True


class BranchOut(BranchBase):
    id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: EmailStr
    phone_number: str
    first_name: str
    last_name: str
    gender: Gender
    role: Role
    user_image: str = (
        "https://media.istockphoto.com/id/1337144146/vector/default-avatar-profile-icon-vector.jpg?s=612x612&w=0&k=20&c=BIbFwuv7FxTWvh5S3vB6bkT0Qv8Vn8N5Ffseq84ClGI="
    )
    date_of_birth: str
    marital_status: MaritalStatus

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: str

    class Config:
        orm_mode = True


class User(UserBase):

    created_at: datetime
    id: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str

    class Config:
        orm_mode = True


class TokenData(BaseModel):
    id: Optional[str] = None

    class Config:
        orm_mode = True


class ServiceBase(BaseModel):
    name: str
    price: int
    is_active: bool

    class Config:
        orm_mode = True


class ServiceCreate(ServiceBase):
    pass

    class Config:
        orm_mode = True


class ServiceOut(ServiceBase):
    id: int

    class Config:
        orm_mode = True


class DoctorBase(BaseModel):
    branch_id: int
    user_id: int

    class Config:
        orm_mode = True


class DoctorCreate(DoctorBase):
    service_id: int

    pass

    class Config:
        orm_mode = True


class DoctorOut(DoctorBase):
    id: int
    branch: BranchOut
    user: User

    class Config:
        orm_mode = True


class DoctorMin(DoctorBase):
    id: int

    class Config:
        orm_mode = True


class PatientBase(BaseModel):
    blood_group: BloodGroup
    address: str
    about: str
    email: EmailStr
    phone_number: str
    first_name: str
    last_name: str
    gender: Gender
    user_image: str = (
        "https://media.istockphoto.com/id/1337144146/vector/default-avatar-profile-icon-vector.jpg?s=612x612&w=0&k=20&c=BIbFwuv7FxTWvh5S3vB6bkT0Qv8Vn8N5Ffseq84ClGI="
    )
    date_of_birth: str
    marital_status: MaritalStatus

    class Config:
        orm_mode = True


class PatientCreate(PatientBase):
    pass

    class Config:
        orm_mode = True


class PatientOut(PatientBase):
    id: int

    class Config:
        orm_mode = True


class PatientLogin(BaseModel):
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None

    class Config:
        orm_mode = True


class AppointmentBase(BaseModel):
    patient_id: int
    doctor_id: int
    service_id: int
    appointment_date: str
    appointment_time: str
    reason: str

    class Config:
        orm_mode = True


class AppointmentCreate(AppointmentBase):
    pass

    class Config:
        orm_mode = True


class AppointmentOut(AppointmentBase):
    id: int
    patient: PatientOut
    doctor: DoctorMin
    service: ServiceOut

    class Config:
        orm_mode = True


class PaymentBase(BaseModel):
    appointment_id: int
    amount: int
    payment_date: str
    payment_mode: str

    class Config:
        orm_mode = True


class PaymentCreate(PaymentBase):
    pass

    class Config:
        orm_mode = True


class PaymentOut(PaymentBase):
    id: int
    appointment: AppointmentOut

    class Config:
        orm_mode = True


class OTP(BaseModel):
    user_id: str
    otp: str

    class Config:
        orm_mode = True
