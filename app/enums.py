from enum import Enum, unique

@unique
class Role(Enum):
    PATIENT = "patient"
    DOCTOR = "doctor"
    ADMIN = "admin"
    SUPER_ADMIN = "super_admin"

@unique
class Gender(Enum):
    MALE ="Male"
    FEMALE="Female"

@unique
class MaritalStatus(Enum):
    SINGLE="Single"
    MARRIED="Married"
    DIVORCED="Divorced"
    WIDOWED="Widowed"


@unique
class BloodGroup(Enum):
    A_POSITIVE="A+"
    A_NEGATIVE="A-"
    B_POSITIVE="B+"
    B_NEGATIVE="B-"
    O_POSITIVE="O+"
    O_NEGATIVE="O-"
    AB_POSITIVE="AB+"
    AB_NEGATIVE="AB-"
