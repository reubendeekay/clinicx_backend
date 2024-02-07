from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from .config import settings
from mailjet_rest import Client


async def send_email(email: str, subject: str, body: str):
    message = Mail(
        from_email="reubenjefwa1@gmail.com",
        to_emails=email,
        subject=subject,
        plain_text_content=body,
    )

    try:
        sg = SendGridAPIClient(settings.sendgrid_api_key)
        response = sg.send(message)
        print(response.body)

        return {"message": "Email sent"}
    except Exception as e:
        print(e)
        return {"message": "Email not sent"}


async def send_user_email(email: str, user: str):
    message = Mail(
        from_email="reubenjefwa1@gmail.com",
        to_emails=email,
    )

    message.dynamic_template_data = {
        "user": user,
    }

    message.template_id = "d-345e4a53e11b4616984889eb4af63b24"

    try:
        sg = SendGridAPIClient(settings.sendgrid_api_key)
        response = sg.send(message)
        print(response.body)

        return {"message": "Email sent"}
    except Exception as e:
        print(e)
        return {"message": "Email not sent"}


async def send_appointment_email(
    email: str, user: str, doctor: str, branch: str, reason: str, date: str, time: str
):
    message = Mail(
        from_email="reubenjefwa1@gmail.com",
        to_emails=email,
    )

    message.dynamic_template_data = {
        "user": user,
        "doctor": doctor,
        "branch": branch,
        "reason": reason,
        "date": date,
        "time": time,
    }

    message.template_id = "d-8f182af754b64786b893a897f47905e9"

    try:
        sg = SendGridAPIClient(settings.sendgrid_api_key)
        response = sg.send(message)
        print(response.body)

        return {"message": "Email sent"}
    except Exception as e:
        print(e)
        return {"message": "Email not sent"}
