from flask import Flask, jsonify, request, render_template
from src import config_reader as cfg
from src.app.services.mail_and_tg import send_telegram_message, send_html_email

app = Flask(__name__)

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


def send_message(type_msg, body, project_name, subject=None, recipients=None):
    """Sends a message via email or Telegram depending on the type."""
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
        data["type"],
        data["body"],
        data["project_name"],
        recipients=data.get("recipients"),
    )
    return (
        jsonify({"success": True, "detail": "Successfully transferred to celery"}),
        200,
    )
