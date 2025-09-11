import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import re
import folium
import webbrowser
import tempfile
import os
import ipinfo

access_token = 'd985d4491f3f03'
handler = ipinfo.getHandler(access_token)

def open_file():
    filepath = filedialog.askopenfilename()
    if filepath:
        file_path_entry.delete(0, tk.END)
        file_path_entry.insert(0, filepath)

def parse_and_map_log_file():
    file_path = file_path_entry.get()
    ip_addresses = set()
    try:
        with open(file_path, 'r') as file:
            output_text.delete(1.0, tk.END)
            for line in file:
                matches = re.findall(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", line)
                ip_addresses.update(matches)
            for ip in ip_addresses:
                output_text.insert(tk.END, f"IP Address: {ip}\n")
        if ip_addresses:
            create_and_show_map(ip_addresses)
    except Exception as e:
        messagebox.showerror("Error", str(e))

def geolocate_ip(ip_address):
    details = handler.getDetails(ip_address)
    if 'loc' in details.all:
        loc = details.all['loc'].split(',')
        latitude, longitude = loc[0], loc[1]
        return latitude, longitude
    return None, None

def create_and_show_map(ip_addresses):
    map_obj = folium.Map(location=[20, 0], zoom_start=2)
    for ip in ip_addresses:
        lat, lon = geolocate_ip(ip)
        if lat and lon:
            folium.Marker([lat, lon], popup=ip).add_to(map_obj)
    with tempfile.NamedTemporaryFile(delete=False, suffix='.html') as tmpfile:
        map_obj.save(tmpfile.name)
        webbrowser.open('file://' + os.path.realpath(tmpfile.name))

root = tk.Tk()
root.title("Log File IP Extractor and Mapper")

file_frame = tk.Frame(root)
file_frame.pack(padx=10, pady=5)

file_path_entry = tk.Entry(file_frame, width=50)
file_path_entry.pack(side=tk.LEFT, padx=(0, 10))

open_button = tk.Button(file_frame, text="Open File", command=open_file)
open_button.pack(side=tk.LEFT)

parse_button = tk.Button(root, text="Parse Log and Show Map", command=parse_and_map_log_file)
parse_button.pack(pady=5)

output_text = scrolledtext.ScrolledText(root, height=15)
output_text.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

root.mainloop()
