import hazelcast
from multiprocessing import Process
from hazelcast import HazelcastError

def task():
    hz = hazelcast.HazelcastClient()
    key = "Pessimistic"
    map = hz.get_map("my-distributed-map").blocking()
    map.put_if_absent(key, 0)
    for i in range(1000):
        try:
            map.lock(key)
            value = map.get(key)
            map.put(key, value + 1)
        except HazelcastError as e:
            print("An error occurred: ", e)
        finally:
            try:
                map.unlock(key)
            except HazelcastError as e:
                print("Failed to unlock: ", e)
    print("Pessimistic Locks: ", map.get(key))

if __name__ == "__main__":
    for _ in range(3):
        Process(target=task).start()