import threading
from copy import deepcopy


print_lock = threading.Lock()


class Router(threading.Thread):

    def __init__(self, ip, network):
        super().__init__()

        self.ip = ip
        self.network = network
        self.neighbors = []
        self.routing_table = {
            ip: {
                "next_hop": ip,
                "metric": 0
            }
        }
        self.next_table = {}

    def add_neighbor(self, router):
        self.neighbors.append(router)

        self.routing_table[router.ip] = {
            "next_hop": router.ip,
            "metric": 1
        }

    def print_table(self, step):
        with print_lock:
            print(f"\nSimulation step {step} of router {self.ip}")
            print(
                f"{'[Source IP]':<18}"
                f"{'[Destination IP]':<18}"
                f"{'[Next Hop]':<18}"
                f"{'[Metric]':<10}"
            )

            for destination, route in sorted(self.routing_table.items()):
                print(
                    f"{self.ip:<18}"
                    f"{destination:<18}"
                    f"{route['next_hop']:<18}"
                    f"{route['metric']:<10}"
                )

    def compute_next_table(self):
        new_table = deepcopy(self.routing_table)

        changed = False

        for neighbor in self.neighbors:
            neighbor_table = neighbor.routing_table

            for destination, route in neighbor_table.items():
                if destination == self.ip:
                    continue
                new_metric = route["metric"] + 1

                if destination not in new_table:
                    new_table[destination] = {
                        "next_hop": neighbor.ip,
                        "metric": new_metric
                    }

                    changed = True

                elif new_metric < new_table[destination]["metric"]:
                    new_table[destination] = {
                        "next_hop": neighbor.ip,
                        "metric": new_metric
                    }

                    changed = True

        self.next_table = new_table
        return changed

    def apply_next_table(self):
        self.routing_table = self.next_table

    def run(self):
        step = 0
        self.print_table(step)
        self.network.barrier.wait()

        while True:
            changed = self.compute_next_table()
            self.network.changes[self.ip] = changed
            self.network.barrier.wait()

            self.apply_next_table()
            step += 1
            self.network.barrier.wait()

            self.print_table(step)
            self.network.barrier.wait()

            if self.ip == sorted(self.network.routers.keys())[0]:
                self.network.converged = not any(self.network.changes.values())
            self.network.barrier.wait()

            if self.network.converged:
                break
            self.network.barrier.wait()

        self.network.barrier.wait()

        with print_lock:
            print(f"\nFinal state of router {self.ip} table:")
            print(
                f"{'[Source IP]':<18}"
                f"{'[Destination IP]':<18}"
                f"{'[Next Hop]':<18}"
                f"{'[Metric]':<10}"
            )

            for destination, route in sorted(self.routing_table.items()):
                print(
                    f"{self.ip:<18}"
                    f"{destination:<18}"
                    f"{route['next_hop']:<18}"
                    f"{route['metric']:<10}"
                )