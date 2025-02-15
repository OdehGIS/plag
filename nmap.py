

# Purpose: Automate the scanning of a host for open ports using Nmap in Python.

import nmap  # Import the Nmap module
import datetime

try:
    # Print student ID
    student_id = "antchr2155"  
    print(f"Student ID: {student_id}")

    # Get the current date and time
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Scan Date & Time: {current_time}")

    # Prompt the user to enter an IP address
    target_host = input("Enter the IP address to scan: ")

    # Initialize the Nmap scanner
    scanner = nmap.PortScanner()

    print(f"Scanning {target_host} for open ports (1-1000)...")

    # Perform the scan from port 1 to 1000
    scanner.scan(target_host, '1-1000')

    # Extract open ports
    open_ports = [port for port in scanner[target_host]['tcp'] if scanner[target_host]['tcp'][port]['state'] == 'open']

    # Store open ports in a tuple
    open_ports_tuple = tuple(open_ports)

    # Print the results
    if open_ports:
        print(f"{target_host} has the following open ports: {open_ports_tuple}")
    else:
        print(f"No open ports found on {target_host} in the range 1-1000.")

except Exception as e:
    print(f"An error occurred: {e}")
