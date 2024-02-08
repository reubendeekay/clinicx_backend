from faker import Faker

fake = Faker()


def verify_if_user(data):
    assert "id" in data
    assert "email" in data
    assert "password" not in data
    assert "phone_number" in data
    assert "first_name" in data
    assert "last_name" in data
    assert "gender" in data
    assert "role" in data
    assert "date_of_birth" in data


def generate_user_data():
    return {
        "email": fake.email(),
        "password": fake.password(),
        "phone_number": fake.phone_number(),
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "gender": "MALE",
        "role": "DOCTOR",
        "date_of_birth": "01/01/1990",
        "marital_status": "SINGLE",
        "user_image": "https://media.istockphoto.com/id/1337144146/vector/default-avatar-profile-icon-vector.jpg?s=612x612&w=0&k=20&c=BIbFwuv7FxTWvh5S3vB6bkT0Qv8Vn8N5Ffseq84ClGI=",
    }


def generate_branch_data():
    return {
        "name": fake.company(),
        "description": fake.text(),
        "address": fake.address(),
        "phone_number": fake.phone_number(),
        "longitude": fake.random_digit(),
        "latitude": fake.random_digit(),
    }


def verify_if_branch(data):
    assert "id" in data
    assert "name" in data
    assert "description" in data
    assert "address" in data
    assert "phone_number" in data
    assert "longitude" in data
    assert "latitude" in data


def generate_appointment_data(patient_id: int, doctor_id: int, service_id: int):
    return {
        "patient_id": patient_id,
        "doctor_id": doctor_id,
        "service_id": service_id,
        "appointment_date": "12/12/2021",
        "appointment_time": "11:30 AM",
        "reason": fake.text(),
    }


def verify_if_appointment(data):
    assert "id" in data
    assert "patient_id" in data
    assert "doctor_id" in data
    assert "service_id" in data
    assert "appointment_date" in data
    assert "appointment_time" in data
    assert "reason" in data
    assert "patient" in data
    assert "doctor" in data
    assert "service" in data


def generate_doctor_data(user_id: int, branch_id: int):
    return {
        "user_id": user_id,
        "branch_id": branch_id,
    }


def verify_if_doctor(data):
    assert "id" in data
    assert "user_id" in data
    assert "branch_id" in data
    assert "user" in data
    assert "branch" in data


def generate_service_data():
    return {
        "name": fake.text(),
        "price": fake.random_number(),
        "is_active": True,
    }


def vefify_if_service(data):
    assert "id" in data
    assert "name" in data
    assert "price" in data


def generate_patient_data():

    return {
        "blood_group": "A+",
        "address": fake.address(),
        "about": fake.text(),
        "email": fake.email(),
        "phone_number": fake.phone_number(),
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "gender": "MALE",
        "user_image": "https://media.istockphoto.com/id/1337144146/vector/default-avatar-profile-icon-vector.jpg?s=612x612&w=0&k=20&c=BIbFwuv7FxTWvh5S3vB6bkT0Qv8Vn8N5Ffseq84ClGI=",
        "date_of_birth": "01/01/1990",
        "marital_status": "SINGLE",
    }


def verify_if_patient(data):
    assert "id" in data
    assert "blood_group" in data
    assert "address" in data
    assert "about" in data
    assert "email" in data
    assert "phone_number" in data
    assert "first_name" in data
    assert "last_name" in data
