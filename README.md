# Message Service

This project provides a message service that allows sending emails and Telegram messages. It integrates Google Gmail API
for sending emails and uses [Python Telegram Bot](https://python-telegram-bot.org/) library for sending Telegram
messages. The project is managed using Celery for asynchronous task processing and Flask as the API server.

## Features

- Send HTML emails to multiple recipients using Gmail API
- Send Telegram messages to multiple recipients
- Asynchronous task handling with Celery and Redis as the broker
- Customizable email and Telegram message templates

## Prerequisites

- Python 3.10 or later
- Redis (for Celery message broker)
- Google API credentials (for Gmail integration)
- Telegram API credentials (for Telethon)

## Installation

1. **Clone the repository**:

    ```bash
    git clone https://github.com/yourusername/messageservice.git
    cd messageservice
    ```

2. **Install dependencies**:

   Using Poetry (make sure Poetry is installed):
    ```bash
    poetry install
    ```

3. **Set up Gmail API credentials**:

- Create a project in the [Google Cloud Console](https://console.cloud.google.com/).
- Enable the Gmail API.
- Download the `credentials.json` file and place it in the root of your project.


4. **Set up Telegram bot**:

- Create bot with [Bot Father](https://t.me/BotFather)
- Copy `BOT_TOKEN` to environment

5. **Configure environment variables**:

   Copy a `example.env` file and past with `.env` name file

## Usage

1. **Run the Flask server**:

    ```bash
    poetry run flask --app src.app.app run --host=0.0.0.0
    ```

   The server will be available at http://127.0.0.1:5000/.

2. **Start the Celery worker**:

   You need to start both the email and Telegram services. You can use the celery-multi command to run both workers:

    ```bash
    celery -A src.app.services.mail_and_tg worker -l info --pool gevent
    ```

3. **Send an email**:

   You can use the `/send-email` endpoint to send an email.

   Example request:

    ```bash
    curl -X POST http://127.0.0.1:5000/send-email \
    -H "Content-Type: application/json" \
    -d '{
    "type": "error",
    "project_name": "Scraper",
    "subject": "Error in Scraper",
    "body": "Error when scrapy web.com: <i>Error description</i>",
    "recipients": ["123@gmail.com", "123@mail.com"]
    }'
    ```

4. **Send a Telegram message**:

   You can use the /send-tg-message endpoint to send a Telegram message.

   Example request:

    ```bash
    curl -X POST http://127.0.0.1:5000/send-tg-message \
    -H "Content-Type: application/json" \
    -d '{
    "recipients": ["111", "222"],
    "type": "info",
    "project_name": "Scraper",
    "subject": "Info from Scraper",
    "body": "Info when scrapy web.com: <i>Info description</i>"
    }'
    ```

## Project Structure

```bash
├── README.md
├── credentials.json # Gmail API credential
├── poetry.lock
├── pyproject.toml # Poetry configuration file
├── src
│   ├── __init__.py
│   ├── app
│   │   ├── __init__.py
│   │   ├── app.py # Flask API entrypoint 
│   │   ├── services # Email and Telegram service logic
│   │   │   ├── __init__.py
│   │   │   └── mail_and_tg.py # Handles email and Telegram sending tasks
│   │   ├── static
│   │   ├── templates # HTML email templates 
│   │   │   ├── error.html
│   │   │   └── info.html
│   │   └── utils.py # Utility functions
│   ├── config_reader.py # Configuration loader
│   ├── example.env # Example environment file
│   └── token_gen.py # Gmail token generator script
└── token.json # Gmail API token file
```

## Endpoints

- `/send-email`: Sends an email with a custom HTML template.
- `/send-tg-message`: Sends a Telegram message to specified recipients.

## Contributing

Feel free to submit issues or pull requests if you want to contribute to this project.

markdown
Копировать код

### Key Sections:

- **Project Overview**: Brief description of the service's purpose.
- **Installation**: Step-by-step instructions on how to install dependencies and set up API credentials.
- **Usage**: Provides examples of how to use the API endpoints.
- **Celery Workers**: Instructions for running multiple Celery workers.
- **Project Structure**: Overview of the project directory layout.