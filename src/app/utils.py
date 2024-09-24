import base64
from email.mime.text import MIMEText
from pathlib import Path


def send_message(service, user_id, message):
    """Send an email message."""
    try:
        message = (
            service.users().messages().send(userId=user_id, body=message).execute()
        )
        print("Message Id: %s" % message["id"])
        return message
    except Exception as error:
        print("An error occurred: %s" % error)


def create_message(sender, to, subject, message_text):
    """Create a message for an email."""
    message = MIMEText(message_text, "html")
    message["to"] = to
    message["subject"] = subject
    b64_bytes = base64.urlsafe_b64encode(message.as_bytes())
    b64_string = b64_bytes.decode()
    return {"raw": b64_string}


def ensure_directory_exists(filename: Path | str) -> None:
    """
    Ensure the directory containing the file exists (create it if necessary).

    :param filename: file.

    """
    Path(filename).parent.mkdir(parents=True, exist_ok=True)
