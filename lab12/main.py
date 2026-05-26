from network import Network


def main():
    network = Network()

    mode = input(
        "Choose mode:\n"
        "1 - Load from config.json\n"
        "2 - Generate random network\n"
    )

    if mode == "1":
        network.load_from_file("config.json")
    else:
        count_v = int(input("Number of routers: "))
        count_e = int(input("Number of edges: "))
        if count_e > count_v * (count_v - 1) / 2:
            print("Too many edges!\n"
                  f"Maximum - {int(count_v * (count_v - 1) / 2)}")
            return
        network.generate_random(count_v, count_e)

    network.start()

if __name__ == "__main__":
    main()