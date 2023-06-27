import hazelcast
import json
import time
import argparse, uuid
import consul
import os
from flask import Flask, jsonify


app = Flask(__name__)

consul_host = "127.0.0.1"
consul_port = 8500
consul_client = consul.Consul(host=consul_host, port=consul_port)

def get_message_queue_settings():
    _, settings = consul_client.kv.get("message_queue_settings")
    if settings:
        return json.loads(settings['Value'])
    else:
        raise Exception("Message Queue settings not found in Consul.")

def register_service(service_name, service_port):
    service_id = str(uuid.uuid4())
    service_ip = os.getenv('SERVICE_IP', 'localhost')
    consul_client.agent.service.register(
        service_name,
        service_id=service_id,
        address=service_ip,
        port=service_port
    )

message_queue_settings = get_message_queue_settings()

hz = hazelcast.HazelcastClient()

queue_name = message_queue_settings["queue_name"]
queue = hz.get_queue(queue_name).blocking()

messages = []

@app.route('/messages', methods=['GET'])
def get_messages():
    messages.clear() # очистка списка сообщений перед добавлением новых
    for i in range(0, 5):
        try:
            message = queue.poll(1)  # добавлен таймаут
            if message is None:
                break
            print(f"Received message '{message}' from Hazelcast")  # Debug line
            messages.append(message)
        except:
            break
    return jsonify({"messages": messages})

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, required=True)
    args = parser.parse_args()

    register_service("messages-service", args.port)

    app.run(port=args.port)
