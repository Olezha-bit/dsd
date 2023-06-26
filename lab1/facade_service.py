from flask import Flask, request, jsonify
import requests
import uuid

app = Flask(__name__)

logging_service = "http://localhost:8081/logging"
messages_service = "http://localhost:8082/messages"

@app.route("/", methods=["POST", "GET"])
def handle_request():
    if request.method == "POST":
        _msg = request.form.get("msg")
        if not _msg:
            return "Message not provided", 400
        _id = str(uuid.uuid4())
        data = {"id": _id, "msg": _msg}
        response = requests.post(logging_service, data=data)
        if response.status_code != 200:
            return f"Logging service error: {response.text}", response.status_code
        return jsonify({"id": _id, "msg": _msg}), 200
    elif request.method == "GET":
        log_response = requests.get(logging_service)
        if log_response.status_code != 200:
            return f"Logging service error: {log_response.text}", log_response.status_code
        msg_response = requests.get(messages_service)
        if msg_response.status_code != 200:
            return f"Messages service error: {msg_response.text}", msg_response.status_code
        return [log_response.text, msg_response.text], 200
    else:
        abort(400)

if __name__ == "__main__":
    app.run(port=8080)
