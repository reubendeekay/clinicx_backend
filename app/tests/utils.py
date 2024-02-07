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
        "gender": "Male",
        "role": "doctor",
        "date_of_birth": "2024-02-04T13:14:12.846Z",
        "marital_status": "Single",
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
