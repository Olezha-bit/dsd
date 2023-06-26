from flask import Flask, jsonify
import hazelcast
import argparse
import threading

app = Flask(__name__)

parser = argparse.ArgumentParser()
parser.add_argument("--port", type=int, required=True)
args = parser.parse_args()

hz = hazelcast.HazelcastClient()

queue_name = "message-queue"
queue = hz.get_queue(queue_name).blocking()

messages = []

def poll_messages():
    while True:
        if not queue.is_empty():
            message = queue.take()
            print(f"Received message: {message}")
            messages.append(message)

@app.route('/messages', methods=['GET'])
def get_messages():
    return jsonify({"messages": messages})

if __name__ == '__main__':
    thread = threading.Thread(target=poll_messages, daemon=True)
    thread.start()
    app.run(port=args.port)
