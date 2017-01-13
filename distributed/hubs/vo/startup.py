from hubs.vo.entry import EntryPoint

def main():
    entry = EntryPoint()
    entry.configure()
    entry.start()

if __name__ == "__main__":
    main()