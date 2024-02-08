from .main import app, user
from fastapi.testclient import TestClient
from faker import Faker
from .tests.utils import (
    verify_if_user,
    generate_user_data,
    generate_branch_data,
    verify_if_branch,
    generate_appointment_data,
    verify_if_appointment,
    generate_doctor_data,
    verify_if_doctor,
    generate_service_data,
    vefify_if_service,
    generate_patient_data,
    verify_if_patient,
)


client = TestClient(app)
fake = Faker()


# TEST UTILS======================================


def create_user():
    user = generate_user_data()
    response = client.post("/users/", json=user)
    print(user)
    assert response.status_code == 201
    return response.json()


def create_user_with_password():
    user = generate_user_data()
    response = client.post("/users/", json=user)

    assert response.status_code == 201
    return user


def create_doctor():
    user = create_user()
    branch = create_branch()
    doctor = generate_doctor_data(user_id=user["id"], branch_id=branch["id"])
    token = login_user()["access_token"]

    response = client.post(
        "/doctors/", json=doctor, headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 201
    return response.json()


def create_branch():
    branch = generate_branch_data()
    token = login_user()["access_token"]
    response = client.post(
        "/branches/", json=branch, headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201
    return response.json()


def create_appointment():
    patient_id = create_patient()["id"]
    doctor_id = create_doctor()["id"]
    service_id = create_service()["id"]

    appointment = generate_appointment_data(
        patient_id=patient_id, doctor_id=doctor_id, service_id=service_id
    )
    token = login_user()["access_token"]
    response = client.post(
        "/appointments/", json=appointment, headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201
    return response.json()


def create_patient():
    patient = generate_patient_data()
    token = login_user()["access_token"]
    response = client.post(
        "/patients/", json=patient, headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201
    return response.json()


def create_service():
    service = generate_service_data()
    token = login_user()["access_token"]
    response = client.post(
        "/services/", json=service, headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201
    return response.json()


def login_user():
    user = create_user_with_password()
    response = client.post(
        "/login/", data={"username": user["email"], "password": user["password"]}
    )
    assert response.status_code == 201
    print(response.json())
    return response.json()


# START OF TESTS=====================


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Clinic X API"}


def test_create_user():
    user = create_user()
    verify_if_user(user)


def test_get_user():
    token = login_user()["access_token"]
    user = create_user()
    response = client.get(
        f"/users/{user['id']}", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    verify_if_user(data)


def test_get_users():
    token = login_user()["access_token"]
    response = client.get("/users/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json() == [] or response.json() is not None
    verify_if_user(response.json()[0])


def test_update_user():
    token = login_user()["access_token"]
    user = create_user()
    new_user = generate_user_data()
    response = client.put(
        f"/users/{user['id']}",
        json=new_user,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200


def test_delete_user():
    token = login_user()["access_token"]
    user = create_user()
    response = client.delete(
        f"/users/{user['id']}", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 204
    response = client.get(
        f"/users/{user['id']}", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}


# BRANCH TESTS


def test_create_branch():
    branch = create_branch()
    verify_if_branch(branch)


def test_get_branch():
    branch = create_branch()
    response = client.get(f"/branches/{branch['id']}")
    assert response.status_code == 200
    data = response.json()
    verify_if_branch(data)


def test_get_branches():
    response = client.get("/branches/")
    assert response.status_code == 200
    assert response.json() == [] or response.json() is not None
    verify_if_branch(response.json()[0])


def test_delete_branch():
    branch = create_branch()
    token = login_user()["access_token"]
    response = client.delete(
        f"/branches/{branch['id']}", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 204
    response = client.get(f"/branches/{branch['id']}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Branch not found"}


# DOCTOR TEST
def test_create_doctor():
    doctor = create_doctor()
    verify_if_doctor(doctor)


def test_get_doctor():
    doctor = create_doctor()
    token = login_user()["access_token"]
    response = client.get(
        f"/doctors/{doctor['id']}", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    verify_if_doctor(data)


def test_get_doctors():
    token = login_user()["access_token"]
    response = client.get("/doctors/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json() == [] or response.json() is not None
    verify_if_doctor(response.json()[0])


def test_delete_doctor():
    doctor = create_doctor()
    token = login_user()["access_token"]
    response = client.delete(
        f"/doctors/{doctor['id']}", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 204


# SERVICE TESTS


def test_create_service():
    service = create_service()
    vefify_if_service(service)


def test_get_service():
    token = login_user()["access_token"]
    service = create_service()
    response = client.get(
        f"/services/{service['id']}", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    vefify_if_service(data)


def test_get_services():
    token = login_user()["access_token"]
    response = client.get("/services/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json() == [] or response.json() is not None
    vefify_if_service(response.json()[0])


def test_delete_service():
    service = create_service()
    token = login_user()["access_token"]
    response = client.delete(
        f"/services/{service['id']}", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 204


# def update_service():
#     token = login_user()["access_token"]
#     service = create_service()
#     new_service = generate_service_data()
#     response = client.put(
#         f"/services/{service['id']}",
#         json=new_service,
#         headers={"Authorization": f"Bearer {token}"},
#     )
#     assert response.status_code == 200


# Patient tests


def test_create_patient():
    patient = create_patient()
    verify_if_patient(patient)


def test_get_patient():
    patient = create_patient()
    token = login_user()["access_token"]
    response = client.get(
        f"/patients/{patient['id']}", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()
    verify_if_patient(data)


def test_get_patients():
    token = login_user()["access_token"]
    response = client.get("/patients/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json() == [] or response.json() is not None
    verify_if_patient(response.json()[0])


def test_delete_patient():
    patient = create_patient()
    token = login_user()["access_token"]
    response = client.delete(
        f"/patients/{patient['id']}", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 204


# APPOINTMENT TESTS


def test_create_appointment():
    appointment = create_appointment()
    verify_if_appointment(appointment)


def test_get_appointment():
    appointment = create_appointment()
    token = login_user()["access_token"]
    response = client.get(
        f"/appointments/{appointment['id']}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    verify_if_appointment(data)


def test_get_appointments():
    token = login_user()["access_token"]
    response = client.get(
        "/appointments/", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json() == [] or response.json() is not None
    verify_if_appointment(response.json()[0])


def test_delete_appointment():
    appointment = create_appointment()
    token = login_user()["access_token"]
    response = client.delete(
        f"/appointments/{appointment['id']}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 204
