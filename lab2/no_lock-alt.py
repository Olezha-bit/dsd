import multiprocessing
import hazelcast

def no_locks():
    hz = hazelcast.HazelcastClient()
    key = "No Locks"
    map = hz.get_map("my-distributed-map").blocking()
    if (map.contains_key(key) is False):
        map.put(key,0)
    for i in range(1000):
        counter = map.get(key)
        counter += 1
        map.put(key, counter)
    print(map.get(key))

if __name__ == "__main__":
    processes = []
    for _ in range(3):
        p = multiprocessing.Process(target=no_locks)
        p.start()
        processes.append(p)

    for p in processes:
        p.join()
