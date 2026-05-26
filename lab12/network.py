import json
import random
import threading

from router import Router


class Network:

    def __init__(self):
        self.routers = {}
        self.barrier = None
        self.changes = {}
        self.converged = False

    def load_from_file(self, filename):

        with open(filename, "r") as f:
            data = json.load(f)

        for ip in data["routers"]:
            self.routers[ip] = Router(ip, self)

        for ip1, ip2 in data["links"]:
            self.routers[ip1].add_neighbor(self.routers[ip2])
            self.routers[ip2].add_neighbor(self.routers[ip1])

    def generate_random(self, router_count=3, edge_count=2):
        ips = []

        for _ in range(router_count):
            ip = ".".join(str(random.randint(1, 254)) for _ in range(4))

            while ip in ips:
                ip = ".".join(str(random.randint(1, 254)) for _ in range(4))

            ips.append(ip)

        for ip in ips:
            self.routers[ip] = Router(ip, self)

        possible_edges = []

        for i in range(router_count):
            for j in range(i + 1, router_count):
                possible_edges.append((ips[i], ips[j]))

        chosen_edges = random.sample(possible_edges, edge_count)

        for ip1, ip2 in chosen_edges:
            self.routers[ip1].add_neighbor(self.routers[ip2])
            self.routers[ip2].add_neighbor(self.routers[ip1])

    def start(self):
        router_count = len(self.routers)

        self.barrier = threading.Barrier(router_count)
        self.changes = {ip: True for ip in self.routers}

        for router in self.routers.values():
            router.start()

        for router in self.routers.values():
            router.join()