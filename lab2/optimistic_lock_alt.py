import hazelcast
from multiprocessing import Process

def task():
    hz = hazelcast.HazelcastClient()
    key = "Optimistic"
    map = hz.get_map("my-distributed-map").blocking()
    map.put_if_absent(key, 0)
    for i in range(1000):
        while True:
            old_value = map.get(key)
            if map.replace_if_same(key, old_value, old_value + 1):
                break
    print("Optimistic Locks: ", map.get(key))

if __name__ == "__main__":
    for _ in range(3):
        Process(target=task).start()