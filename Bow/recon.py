import socket
import threading
import queue

def scan_port(target, port, open_ports):
    """
    Scans a single port on a target IP address.
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)  # Reduced timeout for faster scanning
        result = sock.connect_ex((target, port))
        if result == 0:
            print(f"Port {port} is open")
            open_ports.put(port)
        else:
            print(f"Port {port} is closed")
        sock.close()
    except (socket.error, socket.timeout): # catch both socket errors and timeouts.
        print(f"Port {port} timed out or could not connect")
    except KeyboardInterrupt:
        print("Scan interrupted by user.")
        exit()

def scan_ports(target, num_threads=10):
    """
    Scans all 65535 ports on a target IP address using multiple threads.
    """
    open_ports = queue.Queue()
    threads = []
    port_range = (1, 65535)

    for port in range(port_range[0], port_range[1] + 1):
        thread = threading.Thread(target=scan_port, args=(target, port, open_ports))
        threads.append(thread)
        thread.start()

        if len(threads) >= num_threads:
            for t in threads:
                t.join()
            threads = []

    for t in threads:
        t.join()

    open_ports_list = []
    while not open_ports.empty():
        open_ports_list.append(open_ports.get())

    open_ports_list.sort()
    return open_ports_list

def main():
    """
    Main function to run the port scanner.
    """
    target = input("Enter target IP address: ")
    num_threads = int(input("Enter number of threads (default 10): ") or 10

    print(f"Scanning all ports on {target}...")
    open_ports = scan_ports(target, num_threads)

    if open_ports:
        print("\nOpen ports:")
        for port in open_ports:
            print(port)
    else:
        print("\nNo open ports found.")

if __name__ == "__main__":
    main()