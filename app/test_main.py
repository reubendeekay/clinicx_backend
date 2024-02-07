from .main import app, user
from fastapi.testclient import TestClient
from faker import Faker
from .tests.utils import (
    verify_if_user,
    generate_user_data,
    generate_branch_data,
    verify_if_branch,
)


client = TestClient(app)
fake = Faker()


# Test utils


def create_user():
    user = generate_user_data()
    response = client.post("/users/", json=user)

    assert response.status_code == 201
    return response.json()


def create_branch():
    branch = generate_branch_data()
    response = client.post("/branches/", json=branch)
    assert response.status_code == 201
    return response.json()


def login_user():
    user = create_user()
    response = client.post(
        "/login/", data={"username": user["email"], "password": user["password"]}
    )
    assert response.status_code == 201
    return response.json()


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Clinic X API"}


def test_create_user():
    user = create_user()
    verify_if_user(user)


def test_get_user():
    user = create_user()
    response = client.get(f"/users/{user['id']}")
    assert response.status_code == 200
    data = response.json()
    verify_if_user(data)


def test_get_users():
    response = client.get("/users/")
    assert response.status_code == 200
    assert response.json() == [] or response.json() is not None
    verify_if_user(response.json()[0])


# def test_update_user():
#     user = create_user()
#     new_user = generate_user_data()
#     response = client.put(f"/users/{user['id']}", json=new_user)
#     assert response.status_code == 200
#     data = response.json()
#     verify_if_user(data)
#     assert data["email"] == new_user["email"]
#     assert data["phone_number"] == new_user["phone_number"]
#     assert data["first_name"] == new_user["first_name"]
#     assert data["last_name"] == new_user["last_name"]


def test_delete_user():
    user = create_user()
    response = client.delete(f"/users/{user['id']}")
    assert response.status_code == 204
    response = client.get(f"/users/{user['id']}")
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}
