import imghdr
import os
import smtplib
from email.message import EmailMessage

from dotenv import load_dotenv

load_dotenv()
PASSWORD = os.getenv("API_KEY")
SENDER = "a.volkov2509@gmail.com"
RECEIVER = "a.volkov2509@gmail.com"
def send_email(image_path):
    """
    Sends an email with an attached image.

    Args:
        image_path (str): The path to the image file.

    Raises:
        Exception: If an error occurs while sending the email.

    """
    try:
        email_message = EmailMessage()
        email_message["Subject"] = "new object detected"
        email_message["From"] = SENDER
        email_message["To"] = RECEIVER
        email_message.set_content("Hey, we just saw a new customer!")

        with open(image_path, "rb") as image_file:
            content = image_file.read()

        email_message.add_attachment(content, maintype="image", subtype=imghdr.what("", content))

        with smtplib.SMTP("smtp.gmail.com", 587) as gmail:
            gmail.ehlo()
            gmail.starttls()
            gmail.login(SENDER, PASSWORD)
            gmail.sendmail(SENDER, RECEIVER, email_message.as_string())
    except Exception as e:
        print("An error occurred while sending the email:", str(e))

