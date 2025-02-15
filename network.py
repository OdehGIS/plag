import socket

def scan_ports(host):
    """ Scans ports 1-1000 on a given host and returns a list of open ports """
    open_ports = []
    for port in range(1, 1001):  
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)  
            if s.connect_ex((host, port)) == 0:  
                open_ports.append(port)
    return open_ports

def get_service(port):
    """ Returns common services associated with a port """
    services = {
        20: "FTP Data", 21: "FTP Control", 22: "SSH", 23: "Telnet", 25: "SMTP",
        53: "DNS", 80: "HTTP", 110: "POP3", 143: "IMAP", 443: "HTTPS", 3306: "MySQL"
    }
    return services.get(port, "Unknown Service")

def main():
    """ Main function to handle user input and perform scanning """
    user_input = input("Enter IP addresses (comma-separated): ")
    hosts = user_input.split(',')

    for host in hosts:
        host = host.strip()  
        print(f"\nScanning {host}...")
        open_ports = scan_ports(host)

        if open_ports:
            for port in open_ports:
                print(f"Host: {host}, Port: {port}, Service: {get_service(port)}")
        else:
            print(f"No open ports found on {host}.")

if __name__ == "__main__":
    main()
#192.168.127.10,192.168.127.14,127.0.0.1
