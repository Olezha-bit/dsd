import hazelcast
from flask import Flask, request, abort
import argparse
import subprocess, signal

app = Flask(__name__)

parser = argparse.ArgumentParser()
parser.add_argument("--port", type=int, required=True)
args = parser.parse_args()

p = subprocess.Popen(['./hz-start'])

hz = hazelcast.HazelcastClient()

messages = hz.get_map("messages").blocking()

@app.route("/logging", methods=["POST", "GET"])
def log_request():
    try:
        if request.method == "POST":
            _id = request.form['id']
            _msg = request.form['msg']
            messages.put(_id, _msg)
            print("Received message:", _msg)
            return "Success"
        elif request.method == "GET":
            keys = messages.key_set()
            array = {}  # Initialize the array
            for key in keys:
                value = messages.get(key)
                array[key] = value
            return array
        else:
            abort(400)
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    try:
        app.run(port=args.port)
    except KeyboardInterrupt:
        p.send_signal(signal.SIGINT)
