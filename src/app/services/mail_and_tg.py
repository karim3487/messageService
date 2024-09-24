import asyncio
import os

import telegram
from google.auth.transport._http_client import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from src.app.services import celery_service
from src.app.utils import create_message, send_message
from src.token_gen import SCOPES
from src import config_reader as cfg


@celery_service.task
def send_html_email(message_text, customer_emails, subject, sender):
    CLIENT_SECRET_FILE = "credentials.json"
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    service = build("gmail", "v1", credentials=creds)

    to = ", ".join(customer_emails)
    message = create_message(sender, to, subject, message_text)
    send_message(service, "me", message)


@celery_service.task
def send_telegram_message(recipients, message):
    bot = telegram.Bot(token=cfg.BOT_TOKEN)

    async def send_message():
        for recipient in recipients:
            await bot.send_message(chat_id=recipient, text=message, parse_mode="html")

    asyncio.run(send_message())
