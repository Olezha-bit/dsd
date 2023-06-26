from flask import Flask, request, abort, jsonify
import requests, json
import uuid
import random
import hazelcast

app = Flask(__name__)

queue_name = "message-queue"

hz = hazelcast.HazelcastClient()
queue = hz.get_queue(queue_name).blocking()
i = 0
msg_array = []

@app.route("/", methods=["POST", "GET"])
def handle_request():
    global i
    if request.method == "POST":
        i+=1
        print(i)
        if i==11:
            return "Message not sent", 400
        _msg = request.form.get("msg")
        if not _msg:
            return "Message not provided", 400
        _id = str(uuid.uuid4())
        data = {"id": _id, "msg": _msg}
        port_log = random.randint(8095, 8097)
        logging_service = "http://localhost:{}/logging".format(port_log)
        response = requests.post(logging_service, data=data)
        queue.offer(json.dumps(_msg))
        return jsonify({"id": _id, "msg": _msg}), 200
    elif request.method == "GET":
        i = 0
        port_log = random.randint(8095, 8097)
        log_response = requests.get("http://localhost:{}/logging".format(port_log)).json()
        port_msg = random.randint(8098, 8099)
        msg_response = requests.get("http://localhost:{}/messages".format(port_msg)).json()
        if msg_response not in msg_array:
            msg_array.append(msg_response)
        return jsonify([log_response, msg_array])
    else:
        abort(400)

if __name__ == "__main__":
    app.run(port=8090)
