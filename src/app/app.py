import hashlib
import logging
from flask import Flask, jsonify, request, render_template
from redis import Redis
from src import config_reader as cfg
from src.app.services.mail_and_tg import send_telegram_message, send_html_email

app = Flask(__name__)

redis_client = Redis(host="localhost", port=6379, db=0)

messages_types = ["error", "info"]
required_parameters = ["type", "body", "project_name"]


def validate_request(data):
    """Checks the presence of the required parameters."""
    if not all(key in data for key in required_parameters):
        return False, f"Missing some of required parameters: {required_parameters}"
    if data["type"] not in messages_types:
        return False, f"`type` must be one of: {messages_types}"
    return True, ""


def create_email_message(type_msg, body, project_name):
    """Creates a message for email depending on the type."""
    template_map = {"error": "error.html", "info": "info.html"}
    return render_template(template_map[type_msg], body=body, project_name=project_name)


def generate_message_key(platform, type_msg, body, project_name):
    """Generates a unique key based on the type, body, and project name."""
    msg_str = f"{platform}_{type_msg}_{body}_{project_name}"
    return hashlib.md5(msg_str.encode()).hexdigest()


def send_message(platform, type_msg, body, project_name, subject=None, recipients=None):
    """Sends a message via email or Telegram depending on the type."""
    msg_key = generate_message_key(platform, type_msg, body, project_name)

    # Check if the message key is in Redis (message throttling)
    if redis_client.exists(msg_key):
        logging.info("Message throttled - not sending the same message again.")
        return

    # Set key in Redis with a TTL of 1 hour (3600 seconds)
    redis_client.setex(msg_key, 3600, "sent")

    if subject:
        msg_email = create_email_message(type_msg, body, project_name)
        send_html_email.delay(msg_email, recipients, subject, "")
    elif recipients:
        tg_message = (
            cfg.ERROR_TG_TEMPLATE.format(project_name=project_name, body=body)
            if type_msg == "error"
            else cfg.INFO_TG_TEMPLATE.format(project_name=project_name, body=body)
        )
        send_telegram_message.delay(recipients, tg_message)


@app.route("/send-email", methods=["POST"])
def send_email():
    data = request.json
    is_valid, error_message = validate_request(data)
    if not is_valid:
        return jsonify({"success": False, "detail": error_message}), 400

    send_message(
        "email",
        data["type"],
        data["body"],
        data["project_name"],
        subject=data["subject"],
        recipients=data["recipients"],
    )
    return (
        jsonify({"success": True, "detail": "Successfully transferred to celery"}),
        200,
    )


@app.route("/send-tg-message", methods=["POST"])
def send_tg_message():
    data = request.json
    is_valid, error_message = validate_request(data)
    if not is_valid:
        return jsonify({"success": False, "detail": error_message}), 400

    send_message(
        "tg",
        data["type"],
        data["body"],
        data["project_name"],
        recipients=data.get("recipients"),
    )
    return (
        jsonify({"success": True, "detail": "Successfully transferred to celery"}),
        200,
    )


if __name__ == "__main__":
    app.run(debug=True)
