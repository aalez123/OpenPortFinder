import socket
from concurrent.futures import ThreadPoolExecutor

def scan_port(ip, port):
    """Attempt to connect to a given port on the specified IP address."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(1)  # Set a timeout for the connection attempt
        result = sock.connect_ex((ip, port))  # Try to connect to the port
        return port, result == 0  # Return the port and whether it's open

def scan_ports(ip, start_port, end_port):
    """Scan a range of ports on the specified IP address."""
    open_ports = []
    with ThreadPoolExecutor(max_workers=100) as executor:
        futures = {executor.submit(scan_port, ip, port): port for port in range(start_port, end_port + 1)}
        for future in futures:
            port, is_open = future.result()
            if is_open:
                open_ports.append(port)
                print(f"Port {port} is open")

    return open_ports

# Main execution
if __name__ == "__main__":
    target_ip = input("Enter the IP address to scan: ")  # Get IP address from user
    start_port = 1
    end_port = 1024  # You can adjust this range as needed

    print(f"Scanning {target_ip} for open ports...")
    open_ports = scan_ports(target_ip, start_port, end_port)
    print(f"Open ports: {open_ports}")