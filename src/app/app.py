from flask import Flask, jsonify, request, render_template
from src.app.services.email_service import send_html_email

app = Flask(__name__)

messages_types = ["error", "info"]


@app.route("/send-email", methods=["POST"])
def send_email():
    subject = request.json.get("subject")
    body = request.json.get("body")
    address = request.json.get("address")
    project_name = request.json.get("project_name")
    type_msg = request.json.get("type")
    match type_msg:
        case "error":
            msg_email = render_template(
                "error.html", body=body, project_name=project_name
            )
        case "info":
            msg_email = render_template(
                "info.html", body=body, project_name=project_name
            )
        case _:
            return (
                jsonify(
                    {
                        "error": f"`type` is a required parameter and must take any of these values: {messages_types}"
                    }
                ),
                400,
            )
    send_html_email.delay(msg_email, address, subject, "karim@kloop.kg")
    return jsonify({"success": True})
