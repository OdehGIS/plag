import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox, ttk
import re

def open_file():
    filepath = filedialog.askopenfilename()
    if filepath:
        file_path_entry.delete(0, tk.END)
        file_path_entry.insert(0, filepath)

def parse_log_file():
    file_path = file_path_entry.get()
    selection = parse_type_var.get()
    try:
        with open(file_path, 'r') as file:
            output_text.delete(1.0, tk.END)  # Clear previous content
            for line in file:
                if selection == 'System Events' and re.search(r"\[.+\]", line):
                    output_text.insert(tk.END, line)
                elif selection == 'Warnings' and "DeprecationWarning" in line:
                    output_text.insert(tk.END, line)
                elif selection == 'Version Information' and re.search(r"Version \d+\.\d+\.\d+", line):
                    output_text.insert(tk.END, line)
                elif selection == 'Operational Messages' and ("Starting" in line or "Shutting down" in line):
                    output_text.insert(tk.END, line)
                elif selection == 'IP Addresses':
                    matches = re.findall(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", line)
                    for ip in matches:
                        output_text.insert(tk.END, f"IP Address: {ip}\n")
                elif selection == 'Remote SSH Version':
                    match = re.search(r"Remote SSH version:\s*(SSH-\d+\.\d+-\w+)", line, re.IGNORECASE)
                    if match:
                        version_info = match.group(1)
                        output_text.insert(tk.END, f"Remote SSH Version: {version_info}\n")
                elif selection == 'SSH Client Hassh':
                    match = re.search(r"ssh client hassh fingerprint:\s*([a-f0-9]+)", line, re.IGNORECASE)
                    if match:
                        fingerprint = match.group(1)
                        output_text.insert(tk.END, f"SSH Client Hassh Fingerprint: {fingerprint}\n")
                elif selection == 'Debug Messages':
                    if "debug" in line.lower():
                        output_text.insert(tk.END, line)
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Create the main window
root = tk.Tk()
root.title("Log File Parser")

# Create a frame for the file path input and button
file_frame = tk.Frame(root)
file_frame.pack(padx=10, pady=5)

file_path_entry = tk.Entry(file_frame, width=50)
file_path_entry.pack(side=tk.LEFT, padx=(0, 10))

open_button = tk.Button(file_frame, text="Open File", command=open_file)
open_button.pack(side=tk.LEFT)

# Dropdown menu for selecting what to parse
parse_type_var = tk.StringVar(root)
parse_type_var.set("System Events")  # default value

parse_type_label = tk.Label(root, text="Select category to parse:")
parse_type_label.pack()

parse_type_dropdown = ttk.Combobox(root, textvariable=parse_type_var)
parse_type_dropdown['values'] = ("System Events", "Warnings", "Version Information", "Operational Messages", "IP Addresses", "Remote SSH Version", "SSH Client Hassh", "Debug Messages")
parse_type_dropdown.pack()

# Button to start parsing
parse_button = tk.Button(root, text="Parse Log", command=parse_log_file)
parse_button.pack(pady=5)

# Text area for displaying results
output_text = scrolledtext.ScrolledText(root, height=15)
output_text.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

# Run the application
root.mainloop()
