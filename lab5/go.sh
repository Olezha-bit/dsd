#!/bin/bash

trap 'kill $(jobs -p)' EXIT

curl \                               
    --request PUT \
    --data '{ "cluster_members": ["127.0.0.1:5701", "127.0.0.1:5702", "127.0.0.1:5703"], "cluster_name": "my-cluster", "cluster_password": "my-password" }' \                      
    http://127.0.0.1:8500/v1/kv/hazelcast_settings

curl \                               
    --request PUT \
    --data '{ "cluster_members": ["127.0.0.1:5701", "127.0.0.1:5702", "127.0.0.1:5703"], "cluster_name": "my-cluster", "cluster_password": "my-password", "map_name": "my-map" }' \
    http://127.0.0.1:8500/v1/kv/hazelcast_settings

curl \                               
    --request PUT \
    --data '{ "queue_name": "my-queue" }' \
    http://127.0.0.1:8500/v1/kv/message_queue_settings


python3 logging_service.py --port 9002 &
sleep 5

python3 logging_service.py --port 9003 &
sleep 5

python3 logging_service.py --port 9004 &
sleep 5

python3 messages_service.py --port 9005 &
sleep 5

python3 messages_service.py --port 9006 &
sleep 10

python3 facade_service.py --port 9001 &

wait
