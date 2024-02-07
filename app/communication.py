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
